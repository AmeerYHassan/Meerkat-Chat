# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import models 
import requests
import os
import flask
import flask_sqlalchemy
import flask_socketio
import requests
import random

# Needed to generate names for each user
animals = ["Cat", "Dog", "Elephant", "Serval", "Ocelot", "Giraffe", "Bear", "Panda", "Bird", "Lizard", "Skink", "Fish", "Shark", "Dolphin", "Muskrat", "Ferret", "Sheep"]
adjectives = ["Enjoyable", "Astonishing", "Super", "Amusing", "Large", "Fancy", "Kind", "Delightful", "Eager", "Bright", "Amiable", "Generous", "Playful", "Disgusting"]
takenNames = set()
usernameDict = {}

app = flask.Flask(__name__)

# Establish socket connection
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# Load environment variables
dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

# Set up authentication for psql database
database_uri = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# Initialize database
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

# Method to get responses from the chat bot.
def getBotResponse(message):
    splitMessage = message.split()
    messageResponse = ""
    # If the first part of the message has funtranslate, take the rest of the message and send an API call to the funtranslate API
    if "funtranslate" in splitMessage[0]:
        translateString = " ".join(splitMessage[1:])
        if translateString.replace(' ','').isalpha():
            URLStr = "http://api.funtranslations.com/translate/yoda?text="
            URLStr += translateString.replace(" ", "%20")
            response = requests.get(URLStr)
            if (response.status_code == 200):
                messageResponse = response.json()["contents"]["translated"]
            else:
                messageResponse = "Uh oh! Try again in a few, I can't seem to translate that right now."
        else:
            messageResponse = "Sorry, I only can translate sentences that just contain letters! Try again"
    # If the first part specifies catfact, get a random cat fact from the API and return to the server
    elif "catfact" in splitMessage[0]:
        response = requests.get("https://catfact.ninja/fact")
        if (response.status_code == 200):
            messageResponse = response.json()["fact"]
        else:
            messageResponse = "Uh oh! Try again in a few, I can't seem to get a cat fact right now."
    # Return the current time
    elif "time" in splitMessage[0]:
        messageResponse = "The current time is " + datetime.now().strftime("%H:%M:%S")
    # Return the about section of the bot
    elif "about" in splitMessage[0]:
        messageResponse = "Hi, I'm meerkat, and I'm just a small utility for this chat room! Use !!help to see what I can do!"
    # Return the help section of the bot
    elif "help" in splitMessage[0]:
        messageResponse = "!!funtranslate <message> to translate a message to yoda speech, !!time to get the current time, !!catfact to get a random cat fact, or !!about to learn a bit more about me"
    # If the command is nothing else, then urge the user to use the !!help command to see proper syntax.
    else:
        messageResponse = "Sorry, I don't know that command. Use !!help to see what I can do!"
    
    # Return the final message
    return messageResponse

# Sends all of the messages one by one to the client.
def emit_all_messages():
    # Read all of the entries from the database, put each column in a list
    all_messages = [db_message.message for db_message in db.session.query(models.Messages).all()]
    all_users = [db_username.username for db_username in db.session.query(models.Messages).all()]
    all_bot_status = [db_isBot.isBot for db_isBot in db.session.query(models.Messages).all()]
    
    messageObjects = []
    # Make a list of message objects, iterating through every list using an index.
    for i in range(len(all_messages)):
        currObject = {}
        currObject["message"] = all_messages[i]
        currObject["username"] = all_users[i]
        currObject["isBot"] = all_bot_status[i]
        messageObjects.append(currObject)
    
    # Send each message using socketio to the client.
    for message in messageObjects:
        socketio.emit('message recieved', message)


# On connect, tell the client to increase the user count by one and emit all the messages.
@socketio.on('connect')
def on_connect():
    socketio.emit('user count change', { "changeBy": +1 })
    emit_all_messages()
    print("A user has connected!")

# On disconnect, tell the client to decrease the user count by one.
@socketio.on('disconnect')
def on_disconnect():
    socketio.emit('user count change', { "changeBy": -1 })
    print("A user has disconnected!")

# When a new message is recieved...
@socketio.on('new message')
def new_message(data):
    # Parse the message to see if it's a bot command or a user message. Create an object to hold message contents.
    messageContents = data["message"]
    retObj = {}
    # If it's a bot, call the bot response method and set the object to specify that it's a bot.
    if (messageContents[0:2] == "!!"):
        retObj["message"] = getBotResponse(messageContents)
        retObj["isBot"] = True
        retObj["username"] = "Meerkat Bot"
    # If it's a user, either call their username from the dictionary above or create a username for them.
    else:
        retObj["message"] = messageContents
        retObj["isBot"] = False
        # If they have chatted before, just fetch their username.
        if (flask.request.sid in usernameDict):
            retObj["username"] = usernameDict[flask.request.sid]
        else:
            # If they have not chatted before, then generate a username for them. Add their name to the set to make sure there are no repeats.
            newUser = random.choice(adjectives) + " " + random.choice(animals) + " " + str(random.randint(1, 100))
            while newUser in takenNames:
                newUser = random.choice(adjectives) + " " + random.choice(animals) + " " + str(random.randint(1, 100))
            takenNames.add(newUser)
            usernameDict[flask.request.sid] = newUser
            retObj["username"] = usernameDict[flask.request.sid]
    
    # Write to the database the contents of the message, the username, and whether or not it's a bot message.
    db.session.add(models.Messages(retObj['message'], retObj['username'], retObj['isBot']));
    db.session.commit()
    
    # Emit the message to socket.io
    socketio.emit('message recieved', retObj)
    print(retObj)

# Default root directory of the website.
@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
