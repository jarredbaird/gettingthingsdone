"""SQLAlchemy models for GTD"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from random_item import createRandomTitle
import pdb

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connecting db to provided Flask app."""
    db.app = app
    db.init_app(app)

# class Sessions(db.Model):
#     """This item ends up in your inbox to be refined later"""
#     __tablename__ = "sessions"
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Text, nullable=False)
#     data = db.Column(db.UnicodeText, nullable=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     expiry = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Item(db.Model):
    """This item ends up in your inbox to be refined later"""
    __tablename__ = "items"
    i_id = db.Column(db.Integer, primary_key=True)
    i_title = db.Column(db.Text, nullable=False)
    i_descr = db.Column(db.Text, nullable=True)
    i_dt_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'))
    o_id = db.Column(db.Integer, db.ForeignKey('outcomes.o_id'))
    c_id = db.Column(db.Integer, db.ForeignKey('contexts.c_id'))
    ns_id = db.Column(db.Integer, db.ForeignKey('next_steps.ns_id'))
    ei_id = db.Column(db.Integer, db.ForeignKey('email_items.ei_id'))

    @classmethod
    def generateRandomTitle(cls):
        return createRandomTitle()

    def serialize(self):
        # pdb.set_trace()
        return {
            'i_id': self.i_id,
            'i_title': self.i_title,
            'i_descr': self.i_descr,
            'i_dt_created': self.i_dt_created.isoformat(),
            'u_id': self.u_id,
            'o_id': self.o_id,
            'c_id': self.ns_id,
            'ns_id': self.ns_id,
            'ei_id': self.ei_id
            }

class User(db.Model):
    """User Model"""
    __tablename__ = "users"
    u_id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    u_username = db.Column(db.Text, 
                           nullable=False, 
                           unique=True)
    u_name = db.Column(db.Text)
    password = db.Column(db.Text, 
                         nullable=False)
    u_dt_created = db.Column(db.DateTime, default=datetime.utcnow)
    google_email_address = db.Column(db.Text, unique=True)
    google_access_token = db.Column(db.Text)
    google_token_type = db.Column(db.Text)
    google_refresh_token = db.Column(db.Text)
    google_expires_in = db.Column(db.Integer)
    google_scope = db.Column(db.Text)
    google_history_id = db.Column(db.Integer)

    def serialize(self):
        return {'u_id': self.u_id,
                'active': self.active,
                'u_username': self.u_username,
                'google_access_token': self.google_access_token,
                'google_token_type': self.google_token_type,
                'google_refresh_token': self.google_refresh_token,
                'google_expires_in': self.google_expires_in,
                'google_scope': self.google_scope,
                'u_name': self.u_name,
                'u_dt_created': self.u_dt_created.isoformat()
        }

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        user = User.query.filter_by(u_username=username).first()
        if not user:
            hashed = bcrypt.generate_password_hash(pwd)
            # turn bytestring into normal (unicode utf8) string
            hashed_utf8 = hashed.decode("utf8")

            # return instance of user w/username and hashed pwd
            new_user = cls(u_username=username, password=hashed_utf8)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        else:
            return False

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(u_username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

class Outcome(db.Model):
    """The outcome of a specific item"""
    __tablename__ = "outcomes"
    o_id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.Text, nullable=False)

class NextStep(db.Model):
    """The next step needed to get an item going"""
    __tablename__ = "next_steps"
    ns_id = db.Column(db.Integer, primary_key=True)
    ns_name = db.Column(db.Text, nullable=False)

class EmailItem(db.Model):
    """all the parts of emails that come in"""
    __tablename__ = "email_items"
    ei_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Text)
    send_to = db.Column(db.ARRAY(db.Text))
    cc = db.Column(db.ARRAY(db.Text))
    bcc = db.Column(db.ARRAY(db.Text))
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    thread_id = db.Column(db.Text)

class NextAction(db.Model):
    """the next thing a user should be doing"""
    __tablename__ = "next_actions"
    na_id = db.Column(db.Integer, primary_key=True)
    i_id = db.Column(db.Integer, db.ForeignKey('items.i_id'), nullable=False)
    dt_moved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_viewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class SomedayMaybe(db.Model):
    """things the user may get around to one day"""
    __tablename__ = "someday_maybe"
    sm_id = db.Column(db.Integer, primary_key=True)
    i_id = db.Column(db.Integer, db.ForeignKey('items.i_id'), nullable=False)
    dt_moved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_viewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Calendar(db.Model):
    """date or time specfic calendar items"""
    __tablename__ = "calendar"
    cal_id = db.Column(db.Integer, primary_key=True)
    i_id = db.Column(db.Integer, db.ForeignKey('items.i_id'), nullable=False)
    day = db.Column(db.Boolean, nullable=False, default=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dt_moved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_viewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class WaitingOn(db.Model):
    """Things that the user is waiting on"""
    __tablename__ = "waiting_on"
    wo_id = db.Column(db.Integer, primary_key=True)
    i_id = db.Column(db.Integer, db.ForeignKey('items.i_id'), nullable=False)
    dt_moved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_viewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Reference(db.Model):
    """General library of non-actionable things"""
    __tablename__ = "reference"
    r_id = db.Column(db.Integer, primary_key=True)
    i_id = db.Column(db.Integer, db.ForeignKey('items.i_id'), nullable=False)
    dt_moved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_viewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Context(db.Model):
    """who are you with? where are you? is your kid with you?
    The general scenario in which you should be in order to complete the task"""
    __tablename__ = "contexts"
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Boolean, nullable=False, default=False)

class WorkMode(db.Model):
    """will determine the views / modes a user will be in while completing
    'work'. Can either  be "Doing predefined work", "Doing work as it shows up", 
    or "Defining your work"."""
    __tablename__ = "work_modes"
    wm_id = db.Column(db.Integer, primary_key=True)
    wm_name = db.Column(db.Text, nullable=False)
    wm_view = db.Column(db.Text)
