from flask_restful import Resource, Api

class Oauth(Resource):

    def get(self):
        return {'test':'test route'}
