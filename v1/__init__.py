#FLASK SETTINGS
from flask import Flask, jsonify
app = Flask(__name__)

#CONFIGURATION SETTINGS
app.config.from_object('v1.config.dev_config')

#API SETTINGS
from flask_restful import Resource, Api
api = Api(app)

#DATABASE SETTINGS
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

#BCRYPT SETTINGS
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from v1 import views, models
from v1.oauth import auth

#JWT SETTINGS
from flask_jwt import JWT, jwt_required, current_identity

#Creates authorization endpoint at /v1/user/auth
def authenticate(username, password):
    authuser = models.User.validate(username, password)
    if authuser['status'] is True:
        return authuser['user']

#Used for current_identity variable
def identity(payload):
    user_id = payload['identity']
    return user_id

jwt = JWT(app, authenticate, identity)
