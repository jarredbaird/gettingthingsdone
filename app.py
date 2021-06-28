
import pdb, json, os
from models import db, connect_db, Item
from schema import ItemRequest, ItemResponse
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None
if os.path.exists('token.json'):
    creds = Credentials(client_id=os.environ.get("google_client_id"), 
                        token_uri=os.environ.get("google_token_uri"), 
                        client_secret=os.environ.get("google_client_secret"))
<<<<<<< HEAD
=======

>>>>>>> 56e45e61bc19950ebdc392929e2840281ba6e3c9
service = build('gmail', 'v1', credentials=creds)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///gtd')).replace("://", "ql://", 1)
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
docs.register(AppItems)
docs.register(AppItem)
docs.register(AppRandomItem)