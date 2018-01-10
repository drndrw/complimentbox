# from flask_restful import Resource, Api, reqparse
import os
from v1 import app, config
from flask import request


'''
TEMPORARY UNTIL REACT FRONTEND IS DEVELOPED

This endpoint is designed to work with Google's implicit Oauth2 authorization flow,
by preseting the user with a login form to generate a bearer token. The token, which
does not expire, is used to authenticate and identify users making requests from
a Google Assistant device.

More information at:
https://developers.google.com/actions/identity/oauth2-implicit-flow
'''

# class Oauth(Resource):
#
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('yeah')
#         args = parser.parse_args()
#         print(args)
#         return {'test':'test route','args':args}

@app.route('/v1/oauth')
def implicit_auth():
    client_keys = {'google':'Google'} #Validate client ID (eg. Google, Amazon, etc.)
    missing_args = [] #A list of missing URL arguments (returned to template)

    #URL arguments to parse
    #Client ID (eg. google)
    client_id = request.args.get('client_id') if request.args.get('client_id') in client_keys else missing_args.append('client_id')
    #Redirect URI (client side)
    redirect_uri = request.args.get('redirect_uri') if request.args.get('redirect_uri') == \
        '{}{}'.format(config.dev_config.GOOGLE_REDIRECT_URI,config.dev_config.GOOGLE_PROJECT_ID)  \
        else missing_args.append('redirect_uri')
    #Bookkeeping value; returned unchanged w/ redirect URI
    state = request.args.get('state') if request.args.get('state') else missing_args.append('state')
    #Response type should be 'token'
    response_type = request.args.get('response_type') if request.args.get('response_type') == 'token' \
        else missing_args.append('response_type')

    if len(missing_args) > 0:
        return ' '.join(missing_args)
    else:
        return 'Passed all checks. Enable user login.'
    #Verify client ID
    # if client_id in client_keys:
    #     print('PASSED CLIENT ID: {}'.format(client_id))
    #     if redirect_uri == '{}{}'.format(config.dev_config.GOOGLE_REDIRECT_URI,config.dev_config.GOOGLE_PROJECT_ID):
    #         print('PASSED REDIRECT URL: {}'.format(redirect_uri))
    #         if response_type == 'token':
    #             print('PASSED RESPONSE TYPE: {}'.format(response_type))
    #             return "Passed all checks. Enable user login."

    print(config.dev_config.GOOGLE_PROJECT_ID)
    return "Checks failed. Do not permit user to login"
