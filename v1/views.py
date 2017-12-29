from flask import jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from v1 import api, app, db, models


# @app.route('/')
# def apptest():
#     return jsonify({'test':'hey'})

class Users(Resource):

    # @jwt_required()
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
        print (current_identity)

    @jwt_required()
    def post(self):
        data = request.get_json()
        if data['title'] and data['body'] and data['recipients']:
            try:
                newmessage = models.Messages(str(current_identity), data['title'], data['body'])
                db.session.add(newmessage)
                db.session.commit()
                for recipient in data['recipients']:
                    newrecipient = models.MessagesRecipients(newmessage.id, recipient)
                    db.session.add(newrecipient)
                db.session.commit()
                return {'status':'Message {} has been sent.'.format(newmessage.id)}
            except Exception as e:
                return {'error':'An error has occured.','info':str(e)}
        else:
            return {'error':'Please enter all required fields.'}

class DefaultPage(Resource):

    def get(self):
        return {'status':'this test works','update':'this page was updated','another_update':'christmas day'}

api.add_resource(Users,'/user')
api.add_resource(UserQuery,'/user/<userid>')
api.add_resource(Message,'/messages')
api.add_resource(DefaultPage,'/')
