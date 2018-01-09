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

    #URL arguments to parse
    client_id = request.args.get('client_id') #Client ID (eg. google)
    redirect_uri = request.args.get('redirect_uri') #Redirect URI (client side)
    state = request.args.get('state') #Bookkeeping value; returned unchanged w/ redirect URI
    response_type = request.args.get('response_type') #Response type should be 'token'

    #Verify client ID
    if client_id in client_keys:
        print('PASSED CLIENT ID: {}'.format(client_id))
        if redirect_uri == '{}{}'.format(config.dev_config.GOOGLE_PROJECT_ID,config.dev_config.GOOGLE_RECIRECT_URI):
            print('PASSED REDIRECT URL: {}'.format(redirect_uri))
            if response_type == 'token':
                print('PASSED RESPONSE TYPE: {}'.format(response_type))
                return "Passed all checks. Enable user login."
    print(config.dev_config.GOOGLE_PROJECT_ID)
    return "Checks failed. Do not permit user to login"
