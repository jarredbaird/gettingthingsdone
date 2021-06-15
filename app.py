import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import Item
import pdb, json

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db

app = Flask(__name__)

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

@app.route('/api/items/all', methods=['GET'])
def getAllItems():
    items = [item.serialize() for item in Item.query.all()]
    return json.dumps(items)

@app.route('/api/item/randomItem', methods=['POST'])
def addRandomItem():
    randomItem = Item.generateRandomItem()
    db.session.add(randomItem)
    return jsonify(randomItem.serialize())

@app.route('/api/item', methods=['POST'])
def addItem():
    item = Item(i_title=request.json['title'])
    db.session.add(item)
    return jsonify(item.serialize())