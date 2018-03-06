from flask import request, jsonify, current_app
from v1 import db, models, app, bcrypt
import secrets
from functools import wraps

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

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
class oauth(object):
    def __init__(self, app=None, header_prefix='Bearer'):
        if app:
            print('im running')
            self.header_prefix = header_prefix
            # self.user_id = None
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        print('made it to app phase')
        self.user_id = None

    '''
    Refactor oauth_required() when there is more time - I want to be able to call this method when
    creating an instance of the oauth class. Reference a previous commit (before 2/7/18) to get the
    version of this method that is final
    '''

    @staticmethod
    def oauth_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            header_prefix='Bearer'
            print(auth_header)
            if auth_header:
                # auth_token = auth_header.split('{} '.format(self.header_prefix))[1]
                print('liked auth header')
                auth_token = auth_header.split('{} '.format(header_prefix))[1]
                print("'" + auth_token + "'")
                print(type(auth_token))
                token_check = models.Authorization.validate_token(auth_token)
                if token_check['status']:
                    print('Auth headers exist')
                    # user_id = token_check['user_id']
                    return f(*args, **kwargs)
                print(token_check['detail'])
                return jsonify({'error':'Invalid authorization token.'})
            else:
                print('bad auth header')
                return jsonify({'error':'Missing authorization token.'})
        return decorated_function

    '''
    Temporary method for obtaining user ID from Bearer token - remove when oauth_required()
    is refactored.
    '''

    @staticmethod
    def get_id(header_prefix='Bearer'):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split('{} '.format(header_prefix))[1]
        token_check = models.Authorization.validate_token(auth_token)
        return token_check['user_id']


#Authenticate user and generate access token
class authorize_user_token():

    def __init__(self, username, password):
        self.user = models.User.validate(username, password)
        self.username = User.query.filter(User.username==username)

    #Generates auth token for user. Takes client_id as only parameter (eg. google)
    def create_token(self, client_id):
        if self.user['status']:
            token = secrets.token_urlsafe(16)
            newtoken = models.Authorization(token,self.user['credentials'],client_id)
            db.session.add(newtoken)
            db.session.commit()
            return token
