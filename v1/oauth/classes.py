from flask import request, jsonify
from v1 import db, models, app, bcrypt
import secrets
from functools import wraps

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

#Decorator for oauth required resources
class oauth():
    def __init__(self, header_prefix='Bearer'):
        self.header_prefix = header_prefix
        self.user_id = None

    def oauth_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            print(auth_header)
            if auth_header:
                auth_token = auth_header.split('{} '.format(self.header_prefix))[1]
                token_check = models.Authorization.validate_token(auth_token)
                if token_check['status']:
                    print('Auth headers exist')
                    self.user_id = token_check['user_id']
                    return f(*args, **kwargs)
                return jsonify({'error':'Invalid authorization token.'})
            else:
                return jsonify({'error':'Missing authorization token.'})
        return decorated_function

#Authenticate user and generate access token
class authorize_user_token():

    def __init__(self, username, password):
        self.user = models.User.validate(username, password)

    #Generates auth token for user. Takes client_id as only parameter (eg. google)
    def create_token(self, client_id):
        if self.user['status']:
            token = secrets.token_urlsafe(16)
            newtoken = models.Authorization(token,self.user['credentials'],client_id)
            db.session.add(newtoken)
            db.session.commit()
            return token
