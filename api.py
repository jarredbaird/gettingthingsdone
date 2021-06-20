from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import Item
import pdb, json
from datetime import datetime
import os
from flask_restful import reqparse, abort, Api, Resource
from models import db, connect_db

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///gtd'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "echnidna_eggs")
# toolbar = DebugToolbarExtension(app)
connect_db(app)

CURR_USER_KEY = "curr_user"
# account credentials

@app.route('/')
def home():
    return render_template('home.html')

class AppItems(Resource):
    def get(self):
        items = [item.serialize() for item in Item.query.all()]
        pdb.set_trace()
        return json.dumps(items)

class AppItem(Resource):
    def post(self):
        args = parser.parse_args()
        item = Item(i_title=args['i_title'], 
                    i_dt_created=datetime.now()
                    )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize())

class AppRandomItem(Resource):
    def post(self):
        randomItem = Item(i_title=Item.generateRandomTitle(), 
                        i_dt_created=datetime.now()
                        )
        db.session.add(randomItem)
        db.session.commit()
        return jsonify(randomItem.serialize())

api.add_resource(AppItems, '/api/items/all')
api.add_resource(AppRandomItem, '/api/item/random-item')
api.add_resource(AppItem, '/api/item')