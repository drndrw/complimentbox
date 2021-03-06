from flask import jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from v1.oauth.classes import oauth
from v1 import api, app, db, models, classes
import json
import os
# from v1.oauth.classes import oauth #Google implicit Oauth2

########################
##### LANDING PAGE #####
########################

class DefaultPage(Resource):

    def get(self):
        return {'v1.0':'https://api.complimentbox.com/v1'}

class V1Page(Resource):

    def get(self):
        return {'Users':'https://api.complimentbox.com/v1/user',
                'Individual user':'https://api.complimentbox.com/v1/user/<id>',
                'Messages':'https://api.complimentbox.com/v1/messages',
                'Individual message':'https://api.complimentbox.com/v1/messages/<id>',}

api.add_resource(DefaultPage,'/')
api.add_resource(V1Page,'/v1')

#########################
##### API VERSION 1 #####
#########################

class Users(Resource):

    def get(self):
        users = models.User.query.all()
        if users:
            return jsonify([{'username':user.username,'id':user.id} \
                for user in users])
        else:
            return {'error':'There are no users.'}

    def post(self):
        data = request.get_json()
        print (data)
        if data['username'] and data['password'] and data['email'] and data['first_name'] \
            and data['last_name']:
            try:
                newuser = models.User(data['username'],data['password'],data['email'],data['first_name'],data['last_name'])
                db.session.add(newuser)
                db.session.commit()
                return {'status':'Successfully created {}.'.format(data['username'])}
            except Exception as e:
                return {'error':'An error has occured.','info':str(e)}
        else:
            return {'error':'Please enter all required fields.'}

class UserQuery(Resource):

    @jwt_required()
    def get(self, userid):
        authuser = models.User.query.filter_by(id=userid).first()
        if authuser:
            return {'username': authuser.username, 'id': authuser.id, 'first_name': authuser.first_name, 'last_name': authuser.last_name, 'email': authuser.email}
        else:
            return {'error': 'Invalid user id.'}

class Message(Resource):

    @jwt_required()
    def get(self):
        #Return list of messages recieved for a given user
        msg = classes.Messages_query(current_identity) #Create Messages_query class
        return msg.get_messages() #Get messages for given identity

    @jwt_required()
    def post(self):
        data = request.get_json()
        msg = classes.Messages_query(current_identity) #Create Messages_query class
        return msg.post_messages(data['type'], data['recipients'], data['message'])

class MessageQuery(Resource):

    @jwt_required()
    def get(self, messageid):
        msg = classes.Messages_query(current_identity)
        return msg.get_individual_message(messageid)

    @jwt_required()
    def delete(self, messageid):
        msg = classes.Messages_query(current_identity)
        return msg.delete_individual_message(messageid)

# class Google(Resource):
#
#     @oauth.oauth_required
#     def get(self):
#         return {'test':'success!', 'id': oauth.get_id()}
#
#     @oauth.oauth_required
#     def post(self):
#         user = oauth.get_id()
#         data = request.get_json()
#         msg = classes.Messages_query(user)
#
#         #WELCOME
#         if data['result']['action'] == 'input.welcome':
#             if user:
#                 return {'speech': 'Welcome to Compliment Box, {}! What would you like to do?'.format(msg.username) ,'displayText': 'Welcome to Compliment Box, {}! What would you like to do?'.format(msg.username)}
#             else:
#                 return {'speech': 'Hey there! Thanks for checking out Compliment Box. Please login by going to complimentbox.com.', 'displayText': 'Thank you for checking out Compliment Box! Please visit complimentbox.com to create an account.', 'data':{'google':{'expect_user_response': False}}}
#
#         #READ MESSAGES
#         elif data['result']['action'] == 'input.read_messages':
#             return {'speech': 'Here are your messages, {}! What would you like to do?'.format(msg.username) ,'displayText': 'Here are your messages, {}!'.format(msg.username)}
#         #END CONVERSATION
#         elif data['result']['action'] == 'input.end':
#             return {'speech': 'Goodbye!', 'displayText': 'Goodbye, {}!'.format(msg.username), 'data':{'google':{'expect_user_response': False}}}
#
#         #FALLBACK
#         else:
#             return {'speech': 'Sorry, I didn\'t get that {}'.format(msg.username) ,'displayText': 'Sorry, I didn\'t get that {}'.format(msg.username)}

api.add_resource(Users,'/v1/user')
api.add_resource(UserQuery,'/v1/user/<userid>')
api.add_resource(Message,'/v1/messages')
api.add_resource(MessageQuery,'/v1/messages/<messageid>')
# api.add_resource(Google,'/v1/google')
