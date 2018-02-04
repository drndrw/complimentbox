from v1 import db, models
from v1.models import Messages, MessagesRecipients, User

############################
##### MESSAGES CLASSES #####
############################

class Messages_query():

    def __init__(self, user_id):
        self.user_id = str(user_id)

    #Verify message owner/ recipient is same as current user
    def is_me(self, *args):
        for arg in args:
            if str(arg) == self.user_id:
                return True

    def get_messages(self):
        messages = Messages.query.join(MessagesRecipients, Messages.id == MessagesRecipients.message_id).join(User, Messages.sender == User.id).add_columns(Messages.id, Messages.sender, User.username, MessagesRecipients.read, Messages.message).filter(MessagesRecipients.user_id==self.user_id).all()
        messages_return = []
        for message in messages:
            messages_return.append({'message_id': message[1], 'sender_id': message[2], 'sender_name': message[3], 'read': message[4], 'message': message[5]})
        return messages_return

    def get_individual_message(self, message_id, mark_read=True):
        message = Messages.query.join(MessagesRecipients, Messages.id == MessagesRecipients.message_id).join(User, Messages.sender == User.id).add_columns(Messages.id, Messages.sender, User.username, MessagesRecipients.read, Messages.message, MessagesRecipients.user_id).filter(Messages.id==message_id).filter(MessagesRecipients.user_id==self.user_id).first()
        if message:
            if self.is_me(*[message[2], message[6]]): #Check user is recipient/ sender of message
                if mark_read: #Mark message as read if True
                    pass
                return {'message_id': message[1], 'sender_id': message[2], 'sender_name': message[3], 'read': message[4], 'message': message[5]}
            else:
                return {'error': 'You do not have permission to view this message'}, 403
        else:
            return {'error': 'Message not found'}, 404

    def delete_individual_message(self, message_id):
        message = Messages.query.add_columns(Messages.sender).filter(Messages.id==message_id).first()
        if self.is_me(*[message[1]]):
            Messages.query.filter(Messages.id==message_id).filter(Messages.sender==self.user_id).delete()
            MessagesRecipients.query.filter(MessagesRecipients.message_id==message_id).delete()
            db.session.commit()
            return {'status': 'Deleted', 'message_id': message_id}
        else:
            return {'error': 'You do not have permission to modify this message'}, 403

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
