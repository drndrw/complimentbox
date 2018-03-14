from v1 import api, app, assist, db, models, classes
from flask_assistant import ask, tell

@assist.action('Default Welcome Intent')
def greet_and_start():
    # speech = "Welcome to Compliment box!"
    # return ask(speech)
    resp = ask("Welcome to Compliment Box!")
    resp.card(text='Welcome to Compliment Box! Here we go.',
              title='Compliment Box',
              img_url='http://example.com/image.png'
              )    # resp.link_out('Github Repo', 'https://github.com/treethought/flask-assistant')
    return resp

@assist.action('Read messages')
def greet_and_start():
    # speech = "Welcome to Compliment box!"
    # return ask(speech)
    resp = ask("Here is a message. Would you like to hear another one?")
    resp.card(text='Welcome to Compliment Box! Here we go.',
              title='Compliment Box',
              img_url='http://example.com/image.png'
              )    # resp.link_out('Github Repo', 'https://github.com/treethought/flask-assistant')
    return resp

@assist.action('End conversation')
def end_convo():
    # speech = "Welcome to Compliment box!"
    # return ask(speech)
    resp = tell("Thank you for using Compliment Box. Goodbye!")
    return resp
