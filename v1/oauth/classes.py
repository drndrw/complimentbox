from flask import request
from v1 import models
from cryptography.fernet import Fernet
import secrets

#Decorator will add arg to missing_args if conditions aren't met
class append_missing():
    def __init__(self):
        self.missing_args = []
        self.available_args = {}

    def confirm(self):
        def wrapper(f):
            if f(request.args.get(f.__name__)):
                self.available_args[f.__name__] = request.args.get(f.__name__)
            else:
                self.missing_args.append(f.__name__)
        return wrapper

#Authenticate user and generate access token
class authorize_user_token():

    def __init__(self, username, password):
        self.user = models.User.validate(username, password)

    def create_token(self):
        return token_urlsafe(16)
