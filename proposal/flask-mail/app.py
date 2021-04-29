"""Blogly application."""

from flask import Flask
from flask_mail import Mail, Message
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

app = Flask(__name__)
mail = Mail(app)

app.config['SECRET_KEY'] = 'echnidna_eggs'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "jarredbaird@gmail.com"
app.config['MAIL_PASSWORD'] = "cbqpzghnllzragpr"
mail.init_app(app)

@app.route('/')
def index():
    msg = Message("Hello",
                  sender=("jarjar", "jarredbaird@gmail.com"),
                  recipients=["jarredbaird@gmail.com"])
    assert msg.sender == "jarjar <jarredbaird@gmail.com>"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return "Sent!"

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/read-email')
def read_email():


# account credentials
username = "youremailaddress@provider.com"
password = "yourpassword"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
