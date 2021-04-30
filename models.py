"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connecting db to provided Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"
    u_id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.Text, nullable=False)
    u_name = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

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

class Item(db.Model):
    """This item ends up in your inbox to be refined later"""
    __tablename__ = "items"
    i_id = db.Column(db.Integer, primary_key=True)
    i_name = db.Column(db.Text, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'))
    o_id = db.Column(db.Integer, db.ForeignKey('outcomes.o_id'))
    c_id = db.Column(db.Integer, db.ForeignKey('contexts.c_id'))
    ns_id = db.Column(db.Integer, db.ForeignKey('next_steps.ns_id'))
    ei_id = db.Column(db.Integer, db.ForeignKey('email_items.ei_id'))

class EmailItem(db.Model):
    """all the parts of emails that come in"""
    __tablename__ = "email_items"
    ei_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Text, nullable=False)
    send_to = db.Column(db.ARRAY(db.Text), nullable=False)
    cc = db.Column(db.ARRAY(db.Text), nullable=False)
    bcc = db.Column(db.ARRAY(db.Text), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    html = db.Column(db.Text, nullable=False)

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
