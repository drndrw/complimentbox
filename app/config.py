import os

class config(object):
    SECRET_KEY = os.getenv('SECRET_KEY','samplekey')

class dev_config(config):

    SECRET_KEY = os.getenv('SECRET_KEY','awskey')
    ENGINE = os.getenv('DB_ENGINE','mysql+pymysql')
    USERNAME = os.getenv('DB_USERNAME','root')
    PASSWORD = os.getenv('DB_PASSWORD','password')
    HOST = os.getenv('DB_HOST','localhost')
    PORT = os.getenv('DB_PORT','3306')
    DBNAME = os.getenv('DB_NAME','compliment')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(ENGINE,USERNAME,PASSWORD,HOST,PORT,DBNAME)
