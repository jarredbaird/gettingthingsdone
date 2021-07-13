
import pdb, json, os, requests, base64, eventlet
from helpers import subPub
from marshmallow.fields import Email
from models import db, connect_db, Item, User
from schema import ItemRequest, ItemResponse
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_apispec.annotations import use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import reqparse, Api, Resource
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from datetime import datetime

# Set up the app
app = Flask(__name__)

# config the app
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///gtd')).replace("s://", "sql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "echnidna_eggs")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# set up the api, request parser, and debugtoolbar
cors = CORS(app, resources={"/api/item/email-item/add": {"origins": "*"}})
api = Api(app)
parser = reqparse.RequestParser()
socketio = SocketIO(app, manage_session=False, async_mode='eventlet', logger=True, engineio_logger=True)
Session(app)
connected_clients = {}
debug = DebugToolbarExtension(app)

# Create an APISpec
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Task Pwner',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='3.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

connect_db(app)

@app.route('/')
def home():
    print(f"**************** Home page: {session.get('user_id')} and {session.items()} **********")
    return render_template('home.html')

class Session (MethodResource, Resource):
    def post(self):
        ''' Handle signin/signup. '''
        print(f"**************** Login: {session.get('user_id')} and {session.items()} **********")

        args = json.loads(request.data)
        name = args.get('username')
        pwd = args.get('password')
        if args.get('type') == 'signin':
            user = User.authenticate(name, pwd)
        else:
            user = User.register(name, pwd)
        if user:
            session["user_id"] = user.u_id
            session["google_email_address"] = user.google_email_address
            return jsonify({
                "user_id": session.get("user_id"), 
                "google_email_address": session.get("google_email_address")
                })
        else:
            return jsonify(None)
    
    def get(self):
        ''' Return the session '''
        print(f"**************** Get session: {session.get('user_id')} and {session.items()} **********")

        return jsonify({
                "user_id": session.get("user_id"), 
                "google_email_address": session.get("google_email_address")
                })

    def head(self):
        ''' handle signout '''
        connected_clients.pop(session.get("google_email_address"))
        session.pop("google_email_address")
        session.pop("user_id")
        session.pop("sid")
        return 'OK', 204

    def patch(self):
        return 0
        
class EmailItem(MethodResource, Resource):
    def post(self):
        print(f"**************** Add email item: {session.get('user_id')} and {session.items()} **********")
        # get the request from the subscription to the email topic 
        subPubData = subPub(request.data)
        print(subPubData)
        # pull ONLY MESSAGED ADDED since the last stored history id
        # This means we'll need to get an access token by using a refresh token
        user = User.query.filter_by(google_email_address=subPubData['emailAddress']).first()
        data = {
                'client_id': os.environ.get('google_client_id'),
                'client_secret': os.environ.get('google_client_secret'),
                'refresh_token': user.google_refresh_token,
                'grant_type': 'refresh_token'}
        r = requests.post('https://oauth2.googleapis.com/token', data=data)
        accessJson = json.loads(r.text)
        headers = {'Authorization': 'Bearer {}'.format(accessJson['access_token'])}
        params = {'historyTypes': ['messageAdded'], 'startHistoryId': user.google_history_id}
        history_response = requests.get('https://gmail.googleapis.com/gmail/v1/users/me/history', headers=headers, params=params)
        email_json = json.loads(history_response.text)
        if email_json.get('history'):
            email_id = email_json['history'][0]['messages'][0]['id']
            # email_thread_id = history_response.data['history']['messages']['threadId']
            email_response = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{email_id}", headers=headers)
            email = json.loads(email_response.text)
            if email.get('payload'):
                for header in email['payload']['headers']:
                    if header['name'].lower() == 'subject':
                        item = Item(i_title=header['value'], i_dt_created=datetime.now(), u_id=user.u_id)
                        db.session.add(item)
                        db.session.commit()
                        if user.google_email_address in connected_clients:
                            for socket_session in connected_clients[user.google_email_address]:
                                socketio.emit('new_email_item', item.serialize(), to=socket_session)
                        break
        else:
            print('no history id')
        # after the emails have been received, store the new history id
        user.google_history_id = subPubData['historyId']
        db.session.add(user)
        db.session.commit()
        return 'OK', 200

# @socketio.on('new_email_item')
# def emitNewItem(item):
#     print(request.items())
#     data = {'data': {
#                 'i_title': item['i_title'], 
#                 'i_dt_created': item['i_dt_created'].isoformat()
#                 }
#             }
#     print(data)
#     emit('new_email_item', data)

@socketio.on('connect')
def registerSocketToSession():
    print(f"*****A new session!!! It's {request.sid}*****")
    session['sid'] = request.sid
    if session.get('user_id'):
        connected_user = User.query.get(session['user_id'])
        connected_user_email_address = connected_user.google_email_address
        sid_exists_in_connected_clients = False
        if connected_user_email_address in connected_clients:
            if session.get('sid'):
                print(f"******* SID during session GET request: f{session['sid']}*****")
                for client_sid in connected_clients[connected_user_email_address]:
                    if session['sid'] == client_sid:
                        sid_exists_in_connected_clients = True
                if not sid_exists_in_connected_clients:
                    connected_clients[connected_user_email_address].append(session['sid'])
        elif not connected_user_email_address in connected_clients:
            if session.get('sid'):
                connected_clients[connected_user_email_address] = []
                connected_clients[connected_user_email_address].append(session['sid'])
    print (f"****** SID upon socket connection request: {session['sid']}")


@app.route('/google451aa8ff7f9058a5.html')
def google_verification():
    return render_template('google451aa8ff7f9058a5.html')


class GoogleAuth(MethodResource, Resource):
    def get(self):
        ''' 
        get the gosh-darned google access token 
        and create a watch on the received emails subscription 
        here, we're only gonna grant ourselves access  
        to a read-only scope on the user's gmail account.
        We're also going to request offline access so that we can get a refresh token
        The refresh token will be needed to renew the watch subscription, as the 
        watch subscription authorization persists only for 7 dayz
        '''

        if 'code' not in request.args:
            # Keep trying until we get a 'code' in redirect params. That's gonna be
            # converted into an access token. The access token expires within seconds...
            # ...but that's ok. We only need it long enough to set a watch on a 
            # sub/pub subscription
            
            return redirect("https://accounts.google.com/o/oauth2/v2/auth?" \
                            "scope=https://www.googleapis.com/auth/gmail.readonly&" \
                            "access_type=offline&" \
                            "include_granted_scopes=true&" \
                            "response_type=code&" \
                            "prompt=consent&" \
                            f"redirect_uri={os.environ.get('OAUTH2_REDIRECT')}&" \
                        f"client_id={os.environ.get('google_client_id')}")
        else:
            # if you got a pesky auth code from the oauth2 redirect params, turn that into an access token
            auth_code = request.args.get('code')
            # All the good stuff you have to submit to google's oauth2 api
            data = {'code': auth_code,
                    'client_id': os.environ.get('google_client_id'),
                    'client_secret': os.environ.get('google_client_secret'),
                    'redirect_uri': os.environ.get('OAUTH2_REDIRECT'),
                    'grant_type': 'authorization_code'}
            r = requests.post('https://oauth2.googleapis.com/token', data=data)
            # aha! got it! let's save that refresh token to the db
            credentials = json.loads(r.text)
            # get this user so we can modify it as needed
            user = User.query.get(session['user_id'])
            user.google_refresh_token = credentials['refresh_token']
            headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
            watchData={'topicName': "projects/taskpwner/topics/received-emails", 'labelIds': ["INBOX"]}
            watchResponse = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/watch", headers=headers, data=watchData)
            userResponse = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/profile", headers=headers)
            userJson = json.loads(userResponse.text)
            watchJson = json.loads(watchResponse.text)
            user.google_history_id = watchJson['historyId']
            user.google_email_address = userJson['emailAddress']
            db.session.add(user)
            db.session.commit()
            return redirect('/')

class UpdateUser(MethodResource, Resource):
    def post(self, **kwargs):
        parser.add_argument([*kwargs])
        args = parser.parse_args()
        user = User(google_access_token=args['access_token'],
                    google_expires_in=args['expires_in'],
                    google_token_type=int(args['token_type']),
                    google_scope=args['scope'],
                    google_refresh_token=args['refresh_token'])
        db.session.add(user)
        db.session.commit()
        return user.serialize()

class AppItems(MethodResource, Resource):
    def get(self):
        print(f"**************** Get all items: {session.get('user_id')} and {session.items()} **********")
        items = [item.serialize() for item in Item.query.filter_by(u_id=session['user_id']).all()]
        return items


# @doc(description="A means of accessing a single Item")
# @use_kwargs(ItemRequest, location=('json'))
# @marshal_with(ItemResponse)
class AppItem(MethodResource, Resource):
    def post(self):
        print(f"**************** Create custom item: {session.get('user_id')} and {session.items()} **********")
        submitted_title = json.loads(request.data)
        item = Item(i_title=submitted_title['i_title'], 
                    i_dt_created=datetime.now(),
                    u_id = session["user_id"]
                    )
        db.session.add(item)
        db.session.commit()
        print(jsonify(item.serialize()))
        return jsonify(item.serialize())

    def get(self):
        print(f"**************** Create random item: {session.get('user_id')} and {session.items()} **********")
        randomItem = Item(i_title=Item.generateRandomTitle(), 
                          i_dt_created=datetime.now(),
                          u_id = session["user_id"]
                        )
        db.session.add(randomItem)
        db.session.commit()
        print(jsonify(randomItem.serialize()))
        return jsonify(randomItem.serialize())
        

api.add_resource(AppItems, '/api/items/all')
api.add_resource(AppItem, '/api/item')
api.add_resource(Session, '/api/session')
api.add_resource(GoogleAuth, "/googleoauth2callback")
api.add_resource(EmailItem, '/api/item/email-item/add')
# api.add_resource(EmailWatch, '/api/item/email-item/watch')
# docs.register(EmailWatch)
docs.register(AppItems)
docs.register(AppItem)
docs.register(Session)
docs.register(GoogleAuth)
docs.register(EmailItem)

if __name__ == "__main__":
    socketio.run(app, port=int(os.environ.get('PORT', '5000')))