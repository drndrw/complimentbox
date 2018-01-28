from v1 import db, models
from v1.models import Messages, MessagesRecipients, User

############################
##### MESSAGES CLASSES #####
############################

class Messages_query():

    def __init__(self, user_id):
        self.user_id = str(user_id)

    def get_messages(self):
        messages = Messages.query.join(MessagesRecipients, Messages.id == MessagesRecipients.message_id).add_columns(Messages.id, Messages.sender, MessagesRecipients.read, Messages.message).filter(MessagesRecipients.user_id==self.user_id).all()
        messages_return = []
        for message in messages:
            messages_return.append({'message_id': message[1], 'sender': message[2], 'read': message[3], 'message': message[4]})
        return messages_return

    def get_users(self):
        user_return = User.query.filter(User.id==self.user_id).all()
        return user_return
