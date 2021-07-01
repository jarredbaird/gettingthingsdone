
import pdb, json, os, requests, asyncio
from marshmallow.fields import Email
from models import db, connect_db, Item, User
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

# Set up gmail api auth and the api service
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# creds = None
# if os.path.exists('token.json'):
#     creds = Credentials(client_id=os.environ.get("google_client_id"), 
#                         token_uri=os.environ.get("google_token_uri"), 
#                         client_secret=os.environ.get("google_client_secret"))
# service = build('gmail', 'v1', credentials=creds)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
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
# toolbar = DebugToolbarExtension(app)
connect_db(app)

CURR_USER_KEY = "curr_user"
# account credentials

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/item/email-item/add', methods=['POST'])
def addEmailItem():
    subResponse = request.args.items()
    print (subResponse)
    return 'OK', 200

@app.route('/google451aa8ff7f9058a5.html')
def google_verification():
    return render_template('google451aa8ff7f9058a5.html')

@app.route("/googleoauth2callback")
def googleAuth():
    if 'code' not in request.args:
        return redirect("https://accounts.google.com/o/oauth2/v2/auth?" \
                        "scope=https://www.googleapis.com/auth/gmail.readonly&" \
                        "access_type=offline&" \
                        "include_granted_scopes=true&" \
                        "response_type=code&" \
                        "prompt=consent&" \
                        "redirect_uri=http://127.0.0.1:5000/googleoauth2callback&" \
                       f"client_id={os.environ.get('google_client_id')}")
    else:
        auth_code = request.args.get('code')
        data = {'code': auth_code,
                'client_id': os.environ.get('google_client_id'),
                'client_secret': os.environ.get('google_client_secret'),
                'redirect_uri': "http://127.0.0.1:5000/googleoauth2callback",
                'grant_type': 'authorization_code'}
        r = requests.post('https://oauth2.googleapis.com/token', data=data)
        session['credentials'] = r.text
        credentials = json.loads(session['credentials'])
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        watchData={'topicName': "projects/taskpwner/topics/received-emails", 'labelIds': ["INBOX"]}
        w = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/watch", headers=headers, data=watchData)
        print(w)
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
        items = [item.serialize() for item in Item.query.all()]
        return items

@doc(description="A means of accessing a single Item")
@use_kwargs(ItemRequest, location=('json'))
@marshal_with(ItemResponse)
class AppItem(MethodResource, Resource):
    def post(self, **kwargs):
        parser.add_argument([*kwargs][0])
        args = parser.parse_args()
        item = Item(i_title=args['i_title'], 
                    i_dt_created=datetime.now()
                    )
        db.session.add(item)
        db.session.commit()
        return item.serialize()

class AppRandomItem(MethodResource, Resource):
    def post(self):
        randomItem = Item(i_title=Item.generateRandomTitle(), 
                        i_dt_created=datetime.now()
                        )
        db.session.add(randomItem)
        db.session.commit()
        return randomItem.serialize()

api.add_resource(AppItems, '/api/items/all')
api.add_resource(AppRandomItem, '/api/item/random-item')
api.add_resource(AppItem, '/api/item')
# api.add_resource(EmailWatch, '/api/item/email-item/watch')
# docs.register(EmailWatch)
docs.register(AppItems)
docs.register(AppItem)
docs.register(AppRandomItem)