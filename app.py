import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask import Flask
from flask_mail import Mail, Message
import imaplib
import email
from email.header import decode_header
import webbrowser
import pdb

# from forms import UserAddForm, UserEditForm, LoginForm, MessageForm
from models import db, connect_db

app = Flask(__name__)
mail = Mail(app)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///gtd'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "echnidna_eggs")
toolbar = DebugToolbarExtension(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "jarredbaird@gmail.com"
app.config['MAIL_PASSWORD'] = "cbqpzghnllzragpr"
mail.init_app(app)
connect_db(app)

CURR_USER_KEY = "curr_user"
MAPS_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/23314.json?access_token=pk.eyJ1Ijoic2VhcmNoLW1hY2hpbmUtdXNlci0xIiwiYSI6ImNrN2Y1Nmp4YjB3aG4zZ253YnJoY21kbzkifQ.JM5ZeqwEEm-Tonrk5wOOMw&cachebuster=1616533965014&autocomplete=true"

# account credentials
username = "jarredbaird@gmail.com"
password = "cbqpzghnllzragpr"

@app.route('/')
def home():
    return render_template('focus.html')
# def index():
#     msg = Message("Hello",
#                   sender=("jarjar", "jarredbaird@gmail.com"),
#                   recipients=["jarredbaird@gmail.com"])
#     assert msg.sender == "jarjar <jarredbaird@gmail.com>"
#     msg.html = "<b>testing</b>"
#     mail.send(msg)
#     return "Sent!"

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/read-email')
def read_email():
    return 0

def clean(text):
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
