from v1 import db, models

############################
##### MESSAGES CLASSES #####
############################

class Messages():

    def __init__(self, user_id):
        self.user_id = user_id

    # def get_messages(self):
