import os
from datetime import timedelta

class config(object):
    SECRET_KEY = os.getenv('SECRET_KEY','samplekey')

class dev_config(config):

    SECRET_KEY = os.getenv('SECRET_KEY','awskey')

    #Database configuration
    ENGINE = os.getenv('DB_ENGINE','mysql+pymysql')
    USERNAME = os.getenv('DB_USERNAME','root')
    PASSWORD = os.getenv('DB_PASSWORD','password')
    HOST = os.getenv('DB_HOST','localhost')
    PORT = os.getenv('DB_PORT','3306')
    DBNAME = os.getenv('DB_NAME','compliment')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(ENGINE,USERNAME,PASSWORD,HOST,PORT,DBNAME)

    #Flask JWT configuration
    JWT_AUTH_URL_RULE = os.getenv('JWT_AUTH_URL_RULE','/v1/user/auth') #Change default
    JWT_EXPIRATION_DELTA = os.getenv('JWT_EXPIRATION_DELTA',timedelta(seconds=3000))

    #Oauth configuration
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID','000000000000')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI','https://oauth-redirect.googleusercontent.com/r/')

    #Assistant configuration
    ASSIST_ACTIONS_ON_GOOGLE = os.getenv('ASSIST_ACTIONS_ON_GOOGLE',True)
