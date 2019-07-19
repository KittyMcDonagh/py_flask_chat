import os

# import redirect, to be able to redirect from one route to another
from flask import Flask, redirect

app = Flask(__name__)

# Create an empty list for messages
messages = []

""" Create a function to add user name and messages to the messages list """

def add_messages(username, message):
    """ Use the append method to add username and message to messages """
    messages.append("{}: {}".format(username, message))
    

def get_all_messages():
    """Get all the messages and separate using a 'br' """
    return "<br>".join(messages)

@app.route('/')
def index():
    
    """
    Main page with instructions
    """
    
    return "To return a message use /USERNAME/MESSAGE"
    
@app.route('/<username>')
def user(username):
    """ Display chat messages """
    return "<h1>Welcome, {}</h1>{}".format(username, get_all_messages())
    
@app.route('/<username>/<message>')
def send_message(username, message):
    """ Create a new message and redirect to the chat page """
    add_messages(username, message)
    return redirect("/" + username)
    
#    return "{0}: {1}".format(username, message)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)


