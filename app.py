import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from random_item import createRandomItem
from models import Item
import pdb

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

@app.route('/api/item/randomItem', methods=['GET'])
def getRandomItem():
    return createRandomItem()

@app.route('/api/item', methods=['POST'])
def addItem():
    item = Item(i_title=request.json['title'])
    db.session.add(item)
    item_json = jsonify(item.serialize())
    return item_json