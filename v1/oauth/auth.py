# from flask_restful import Resource, Api, reqparse
import os
from v1 import app, config
from flask import request
from v1.oauth.classes import append_missing

'''
TEMPORARY UNTIL REACT FRONTEND IS DEVELOPED

This endpoint is designed to work with Google's implicit Oauth2 authorization flow,
by preseting the user with a login form to generate a bearer token. The token, which
does not expire, is used to authenticate and identify users making requests from
a Google Assistant device.

More information at:
https://developers.google.com/actions/identity/oauth2-implicit-flow
'''

@app.route('/v1/oauth')
def implicit_auth():
    client_keys = {'google':'Google'} #Validate client ID (eg. Google, Amazon, etc.)
    missing_args = [] #A list of missing URL arguments (returned to template)

    missing = append_missing()

    #Client ID (eg. google)
    @missing.confirm()
    def client_id(req):
        if req in client_keys:
            return req

    #Redirect URI (client side)
    @missing.confirm()
    def redirect_uri(req):
        if req == '{}{}'.format(config.dev_config.GOOGLE_REDIRECT_URI,config.dev_config.GOOGLE_PROJECT_ID):
            return req

    #Bookkeeping value; returned unchanged w/ redirect URI
    @missing.confirm()
    def state(req):
        if req:
            return req

    #Response type should be 'token'
    @missing.confirm()
    def response_type(req):
        if req == 'token':
            return req

    if len(missing.missing_args) > 0:
        return ' '.join(missing.missing_args)
    else:
        return str(missing.available_args)
