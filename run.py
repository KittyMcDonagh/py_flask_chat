import os

# Import the datetime from the datetime library, which is a built in module in
# Python's standard library that allows us to work specifically with dates and
# times
from datetime import datetime

# import redirect, to be able to redirect from one route to another
# Import render_template to be able to render .html pages
# Import request to handle our username form, and session, which will handle the
# session variables
# Import url_for
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

""" To generate a session id wee need to give our app what's called a secret_key
    key, which is a random list of letters, numbers, and characters. 
    In production we'd have it as an environment variable, but for now we'll put
    it as a string. """
    
    # Make the secret key an environment variable. "randomstring123" becomes the
    # default value, if flask cant find a variable called SECRET.
app.secret_key = os.getenv('SECRET', "randomstring123")

# Create an empty list for messages
messages = []

""" Create a function to add user name and messages to the messages list """

def add_message(username, message):
    """ Use the append method to add username and message to messages """
    now = datetime.now().strftime("%H:%M:%S")
    
    """ append the messages in dictionary format - key:value """
    messages.append({"timestamp": now, "from": username, "message": message})
    
#    messages.append("({}) {}: {}".format(now, username, message))
    
""" get_all_messages fundtion is not going to be referred to anymore 
def get_all_messages():
    # Get all the messages and separate using a 'br'
    return "<br>".join(messages) """

# Add methods to the route
@app.route('/', methods = ["GET", "POST"])
def index():
    
    """ If the program is just loading, then no request yet via index.html form,
        so request method wont be set to "POST". It'll load index.html and 
        display the form felds """
    
    if request.method == "POST":
        session["username"] = request.form["username"]
    
    """ If the username variable is set, redirect to 
        @app.route('/<username>') below, otherwise open
        index.html. Because username is stored in a cookie, it will always
        open the username page. This cookie will be deleted when the browser
        is closed."""
        
    if "username" in session:
        return  redirect(url_for("user", username = session["username"]))
    #    return redirect("/" + session["username"])
        
    """
    Main page with instructions
    """
    
    return render_template('index.html')
    
#    return "To return a message use /USERNAME/MESSAGE"
    
@app.route('/chat/<username>', methods = ["GET", "POST"])
def user(username):
    """ Add and Display chat messages  """
    
    """ To make things neater, create a form in chat.html with a textarea and 
        enter the message. """
    
    # if a message has been sent:
    
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        
        # if we were to let it render_template, as below, it would continuously 
        # display the message multiple times
        return  redirect(url_for("user", username = session["username"]))
        
    """ Otherwise, render the page, showing the textbox, and messages already entered """
            
    return render_template("chat.html", username = username, chat_messages = messages)
    
   #  return "<h1>Welcome, {}</h1>{}".format(username, messages)
    


app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "5000")), debug=True)


