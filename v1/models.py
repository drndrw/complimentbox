from v1 import app, bcrypt, db
from flask import jsonify
import datetime
import string
import random

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    permission = db.Column(db.SmallInteger, nullable=False)
    time_created = db.Column(db.Time, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    # user_messages = db.relationship('Messages')
    # user_recipients = db.relationship('MessagesRecipients')

    def __init__(self, username, password, email, first_name, last_name, permission=1, id=None, time=datetime.datetime.now().time(), date=datetime.datetime.now().date()):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.permission = permission
        self.id = id
        self.time_created = db.Column(db.Time, nullable=False)
        self.date_created = db.Column(db.Date, nullable=False)

    @staticmethod
    def validate(username, password):
        try:
            authuser = User.query.filter_by(username=username).first()
            pwauth = bcrypt.check_password_hash(authuser.password, password)
            if authuser and pwauth:
                return {'status': True, 'credentials': authuser.id, 'user': authuser}
            else:
                return {'status': False, 'failed': 'Invalid password.'}
        except:
            return {'status': False, 'failed': 'Invalid username.'}

class Authorization(db.Model):
    __tablename__ = 'user_authorization'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cliend_id = db.Column(db.String(255), nullable=False)
    time_created = db.Column(db.Time, nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    def __init__(self, access_token, user_id, client_id, id=None, time=datetime.datetime.now().time(), date=datetime.datetime.now().date()):
        self.id = id
        self.access_token = access_token
        self.user_id = user_id
        self.client_id = client_id
        self.time_created = time
        self.date_created = date

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_type = db.Column(db.String(255))
    message = db.Column(db.UnicodeText, nullable=False)
    time_created = db.Column(db.Time, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    messages_messagesrecipients = db.relationship('MessagesRecipients')

    def __init__(self, sender, title, body, id=None, time=datetime.datetime.now().time(), date=datetime.datetime.now().date()):
        self.sender = sender
        self.title = title
        self.body = body
        self.id = id
        self.time_created = time
        self.date_created = date

class MessagesRecipients(db.Model):
    __tablename__ = 'messages_recipients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    read = db.Column(db.Boolean, nullable=False)

    def __init__(self, message_id, user_id, id=None, read=False):
        self.message_id = message_id
        self.user_id = user_id
        self.id = id
        self.read = read

# Populate database with tables. NOT FOR PRODUCTION ENVIRONMENT
@app.route('/create')
def create_tables():
    try:
        db.create_all()
        return jsonify({'status':'Tables have been created.'})
    except Exception as e:
        return jsonify({'error':str(e)})
