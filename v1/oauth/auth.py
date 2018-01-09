# from flask_restful import Resource, Api, reqparse
from v1 import app
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
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')
    response_type = request.args.get('response_type')
    if client_id in client_keys:
        return "Match"
    print(client_id)
    return "Nada"
