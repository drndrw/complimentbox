# from flask_restful import Resource, Api, reqparse
import os
from v1 import app, config, models
from flask import request, render_template, jsonify
from v1.oauth.classes import append_missing, authorize_user_token
import urllib2

'''
TEMPORARY UNTIL REACT FRONTEND IS DEVELOPED

This endpoint is designed to work with Google's implicit Oauth2 authorization flow,
by preseting the user with a login form to generate a bearer token. The token, which
does not expire, is used to authenticate and identify users making requests from
a Google Assistant device.

More information at:
https://developers.google.com/actions/identity/oauth2-implicit-flow
'''

@app.route('/v1/oauth', methods=['GET','POST'])
def implicit_auth():
    if request.method == 'GET':
        client_keys = {'google':'Google'} #Validate client ID (eg. Google, Amazon, etc.)
        missing_args = [] #A list of missing URL arguments (returned to template)
        authorize_post = False #Must be True to permit POST request from this method

        missing = append_missing()

        #Client ID (eg. google)
        @missing.confirm()
        def client_id(req):
            if req in client_keys:
                return req

        #Redirect URI (client side)
        @missing.confirm()
        def redirect_uri(req):
            # if req == '{}{}'.format(config.dev_config.GOOGLE_REDIRECT_URI,config.dev_config.GOOGLE_PROJECT_ID):
            # if req == config.dev_config.GOOGLE_REDIRECT_URI:
            if req:
                return req

        #Bookkeeping value; returned unchanged w/ redirect URI
        @missing.confirm()
        def state(req):
            if req:
                return req
            else:
                return 'sample'

        #Response type should be 'token'
        @missing.confirm()
        def response_type(req):
            if req == 'token':
                return req

        if len(missing.missing_args) > 0:
            authorize_post = True
            return render_template('auth.html', data={'status':False, 'missing_parameters': missing.missing_args})
        else:
            return render_template('auth.html', data={'status':True,'service':client_keys[missing.available_args['client_id']], 'state': missing.available_args['state']})

    if request.method == 'POST':
        data = request.get_json()
        print(data)
        user = authorize_user_token(data['username'], data['password'])
        token = user.create_token(data['service'])
        if token:
            # return jsonify({'status':True,'payload':'{}{}#access_token={}&token_type=bearer&state={}'.format( \
            # config.dev_config.GOOGLE_REDIRECT_URI,config.dev_config.GOOGLE_PROJECT_ID,token,data['state'])})
            return jsonify({'status': True, 'payload': '{}#access_token={}'.format(urllib2.unquote(config.dev_config.GOOGLE_REDIRECT_URI),token)})
        else:
            return jsonify({'status':False})
