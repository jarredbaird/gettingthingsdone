
import pdb, json, os, requests, base64
from marshmallow.fields import Email
from models import db, connect_db, Item, User
from flask_socketio import SocketIO, emit
from schema import ItemRequest, ItemResponse
from flask import Flask, render_template, request, redirect, session, jsonify, g
from flask_apispec.annotations import use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import reqparse, Api, Resource
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from sqlalchemy.exc import IntegrityError
# from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Set up the app, api, and request parser
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
socketio = SocketIO(app, async_mode=None)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///gtd')).replace("s://", "sql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "echnidna_eggs")

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
    return render_template('home.html')

@app.route("/signup", methods=["POST"])
def signup():
    """Register user: produce form & handle form submission."""

    response = json.loads(request.data)
    name = response.get('username')
    pwd = response.get('password')
    user = User.register(name, pwd)
    if user:
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.u_id
        return user.serialize()
    else:
        return jsonify({"message": "User Exists"})


@app.route("/signin", methods=["POST"])
def signin():
    """Produce login form or handle login."""

    response = json.loads(request.data)
    name = response.get('username')
    pwd = response.get('password')
    user = User.authenticate(name, pwd)
    if user:
        session["user_id"] = user.u_id
        return user.serialize()
    else:
        return jsonify({"message": "invalid user"})
        
@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id")
    return redirect('/')

@app.route('/api/item/email-item/add', methods=['POST'])
def addEmailItem():
    # get the request from the subscription to the email topic 
    subRequest = json.loads(request.data)
    print(subRequest)
    # convert message.data from a b64-like string to a decoded string
    subPubDataByteLikeString = subRequest['message']['data']
    subPubDataB64 = subPubDataByteLikeString.encode('utf-8')
    subPubData = base64.b64decode(subPubDataB64).decode('utf-8')
    # pull ONLY MESSAGED ADDED since the last stored history id
    user = User.query.get(session['user_id'])
    headers = {'Authorization': 'Bearer {}'.format(json.loads(session['credentials']['access_token']))}
    params = {'historyTypes': ['messageAdded'], 'startHistoryId': user.google_history_id}
    history_response = requests.get('https://gmail.googleapis.com/gmail/v1/users/me/history', headers=headers, params=params)
    email_id = history_response.data['history']['messages']['id']
    # email_thread_id = history_response.data['history']['messages']['threadId']
    email = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{email_id}", headers=headers)
    print(email)
    # after the emails have been received, store the new history id
    user.google_history_id = subPubData['historyId']
    db.session.add(user)
    db.session.commit()
    return 'OK', 200

@app.route('/google451aa8ff7f9058a5.html')
def google_verification():
    return render_template('google451aa8ff7f9058a5.html')

@app.route("/googleoauth2callback")
def googleAuth():
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
                        "redirect_uri=https://task-pwner.herokuapp.com/googleoauth2callback&" \
                       f"client_id={os.environ.get('google_client_id')}")
    else:
        # if you got a pesky code from the oauth2 redirect params, turn that into an access token
        auth_code = request.args.get('code')
        # All the good stuff you have to submit to google's oauth2 api
        data = {'code': auth_code,
                'client_id': os.environ.get('google_client_id'),
                'client_secret': os.environ.get('google_client_secret'),
                'redirect_uri': "https://task-pwner.herokuapp.com/googleoauth2callback",
                'grant_type': 'authorization_code'}
        r = requests.post('https://oauth2.googleapis.com/token', data=data)
        # aha! got it! let's save that access token to the session
        # Fyi to myself: saving to the session might not be necessary because the token
        # expires so quickly. Refresh token definitely needs to be saved to the db, however,
        # that might not even need to be saved to the session because it is accessed so seldomly
        session['credentials'] = r.text
        credentials = json.loads(session['credentials'])
        # get this user so we can modify it as needed
        user = User.query.get(session['user_id'])
        user.google_access_token = credentials['access_token']
        user.google_refresh_token = credentials['refresh_token']
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        watchData={'topicName': "projects/taskpwner/topics/received-emails", 'labelIds': ["INBOX"]}
        w = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/watch", headers=headers, data=watchData)
        user.google_history_id = w.data['historyId']
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
        items = [item.serialize() for item in Item.query.filter_by(u_id=session['user_id']).all()]
        return items

class Session(MethodResource, Resource):
    def get(self):
        return session

@doc(description="A means of accessing a single Item")
@use_kwargs(ItemRequest, location=('json'))
@marshal_with(ItemResponse)
class AppItem(MethodResource, Resource):
    def post(self, **kwargs):
        parser.add_argument([*kwargs][0])
        args = parser.parse_args()
        item = Item(i_title=args['i_title'], 
                    i_dt_created=datetime.now(),
                    u_id = session["user_id"]
                    )
        db.session.add(item)
        db.session.commit()
        return item.serialize()

class AppRandomItem(MethodResource, Resource):
    def post(self):
        randomItem = Item(i_title=Item.generateRandomTitle(), 
                          i_dt_created=datetime.now(),
                          u_id = session["user_id"]
                        )
        db.session.add(randomItem)
        db.session.commit()
        return randomItem.serialize()

api.add_resource(AppItems, '/api/items/all')
api.add_resource(AppRandomItem, '/api/item/random-item')
api.add_resource(AppItem, '/api/item')
api.add_resource(Session, '/api/user')
# api.add_resource(EmailWatch, '/api/item/email-item/watch')
# docs.register(EmailWatch)
docs.register(AppItems)
docs.register(AppItem)
docs.register(AppRandomItem)