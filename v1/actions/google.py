# from v1 import api, app, assist, db, models, classes
from flask_assistant import ask, tell
from v1.oauth.classes import oauth
from v1 import api, app, assist, db, models, classes
from v1.classes import Messages_query

@oauth.oauth_required
@assist.action('Default Welcome Intent')
def greet_and_start():
    # speech = "Welcome to Compliment box!"
    user = oauth.get_id()
    msg = Messages_query(user)
    # return ask(speech)
    resp = ask("Welcome to Compliment Box, {}!".format(msg.username))
    resp.card(text='Welcome to Compliment Box! Here we go.',
              title='Compliment Box',
              img_url='http://example.com/image.png'
              )    # resp.link_out('Github Repo', 'https://github.com/treethought/flask-assistant')
    return resp

@assist.action('Read messages')
def read_msg():
    # speech = "Welcome to Compliment box!"
    user = oauth.get_id()
    msg = Messages_query(user)
    message_ids = msg.get_latest_message_id()
    try:
        if len(message_ids) > 1:
            recieved_message = msg.get_individual_message(message_ids[0].message_id)
            resp = ask(recieved_message[0]['message'])
            resp.card(text='Message #{}'.format(message_ids[0].id),
                      title='Message #{}'.format(message_ids[0].id),
                      img_url='http://example.com/image.png'
                      )
        else:
            recieved_message = msg.get_individual_message(message_ids[0].message_id)
            resp = ask(recieved_message[0]['message'] + " You have no more messages. What would you like to do now?")
    except Exception as e:
        print(e)
        resp = ask("You have no messages. What would you like to do now?")
    return resp

@assist.action('Write messages')
def write_msg():

@assist.action('End conversation')
def end_convo():
    # speech = "Welcome to Compliment box!"
    # return ask(speech)
    resp = tell("Thank you for using Compliment Box. Goodbye!")
    return resp
