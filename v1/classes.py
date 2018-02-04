from v1 import db, models
from v1.models import Messages, MessagesRecipients, User

############################
##### MESSAGES CLASSES #####
############################

class Messages_query():

    def __init__(self, user_id):
        self.user_id = str(user_id)

    def get_messages(self):
        messages = Messages.query.join(MessagesRecipients, Messages.id == MessagesRecipients.message_id).join(User, Messages.sender == User.id).add_columns(Messages.id, Messages.sender, User.username, MessagesRecipients.read, Messages.message).filter(MessagesRecipients.user_id==self.user_id).all()
        messages_return = []
        for message in messages:
            messages_return.append({'message_id': message[1], 'sender_id': message[2], 'sender_name': message[3], 'read': message[4], 'message': message[5]})
        return messages_return

    def get_individual_message(self, message_id):
        message = Messages.query.join(MessagesRecipients, Messages.id == MessagesRecipients.message_id).join(User, Messages.sender == User.id).add_columns(Messages.id, Messages.sender, User.username, MessagesRecipients.read, Messages.message).filter(Messages.id==message_id).first()
        return {'message_id': message[1], 'sender_id': message[2], 'sender_name': message[3], 'read': message[4], 'message': message[5]}

    def post_messages(self, message_type, message_recipients, message):
        try:
            if message_type and message_recipients and message:
                new_message = models.Messages(self.user_id, message_type, message)
                db.session.add(new_message)
                db.session.commit()
                for recipient in message_recipients:
                    new_recipient = models.MessagesRecipients(new_message.id, recipient)
                    db.session.add(new_recipient)
                db.session.commit()
                return {'status': 'Created', 'type': message_type, 'recipients': message_recipients}
            else:
                return {'error': 'Missing parameters'}
        except Exception as e:
            return {'error': str(e)}

    def get_users(self):
        user_return = User.query.filter(User.id==self.user_id).all()
        return user_return
