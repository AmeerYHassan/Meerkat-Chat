# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import models 
import os
import flask
import flask_sqlalchemy
import flask_socketio
import requests
import random

usernameDict = {}

app = flask.Flask(__name__)

# Establish socket connection
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# Load environment variables
dotenv_path = join(dirname(__file__), 'api_keys.env')
load_dotenv(dotenv_path)

# Set up authentication for psql database
database_uri = os.environ.get('DATABASE_URL')
giphy_key = os.environ.get('GIPHY_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# Initialize database
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

# Method to get responses from the chat bot.
def getBotResponse(returnObject, message):
    splitMessage = message.split()
    # If the first part of the message has funtranslate, take the rest of the message and send an API call to the funtranslate API
    if "funtranslate" in splitMessage[0]:
        translateString = " ".join(splitMessage[1:])
        if translateString.replace(' ','').isalpha():
            URLStr = "http://api.funtranslations.com/translate/yoda?text="
            URLStr += translateString.replace(" ", "%20")
            response = requests.get(URLStr)
            if (response.status_code == 200):
                returnObject["message"] = response.json()["contents"]["translated"]
            else:
                returnObject["message"] = "Uh oh! Try again in a few, I can't seem to translate that right now."
        else:
            returnObject["message"] = "Sorry, I only can translate sentences that just contain letters! Try again"
    # If the first part specifies catfact, get a random cat fact from the API and return to the server
    elif "catfact" in splitMessage[0]:
        response = requests.get("https://catfact.ninja/fact")
        if (response.status_code == 200):
            returnObject["message"] = response.json()["fact"]
        else:
            returnObject["message"] = "Uh oh! Try again in a few, I can't seem to get a cat fact right now."
    # Return a gif if giphy is in the command.
    elif "giphy" in splitMessage[0]:
        requestUrl = "https://api.giphy.com/v1/gifs/search?api_key=" + giphy_key + "&q="+ splitMessage[1] + "&limit=10&offset=0&rating=g&lang=en"
        response = requests.get(requestUrl)
        if (response.status_code == 200):
            returnObject["hasImage"] = True
            returnObject["imageLink"] = random.choice(response.json()["data"])["images"]["original"]["url"]
        else:
            returnObject["message"] = "Uh oh! Try again in a few, I can't seem to get a gif right now."
    # Return the current time
    elif "time" in splitMessage[0]:
        returnObject["message"] = "The current time is " + datetime.now().strftime("%H:%M:%S")
    # Return the about section of the bot
    elif "about" in splitMessage[0]:
        returnObject["message"] = "Hi, I'm meerkat, and I'm just a small utility for this chat room! Use !!help to see what I can do!"
    # Return the help section of the bot
    elif "help" in splitMessage[0]:
        returnObject["message"] = "!!funtranslate <message> to translate a message to yoda speech, !!time to get the current time, !!catfact to get a random cat fact, , !!giphy <query> to retrieve a gif, or !!about to learn a bit more about me"
    # If the command is nothing else, then urge the user to use the !!help command to see proper syntax.
    else:
        returnObject["message"] = "Sorry, I don't know that command. Use !!help to see what I can do!"
    
    # Return the final message
    return returnObject

# Sends all of the messages one by one to the client.
def emit_all_messages():
    # Read all of the entries from the database, put each column in a list
    all_messages = [db_message.message for db_message in db.session.query(models.Messages).all()]
    all_users = [db_username.username for db_username in db.session.query(models.Messages).all()]
    all_bot_status = [db_isBot.isBot for db_isBot in db.session.query(models.Messages).all()]
    all_profile_pictures = [db_profilePicture.profilePicture for db_profilePicture in db.session.query(models.Messages).all()]
    all_hasImage = [db_hasImage.hasImage for db_hasImage in db.session.query(models.Messages).all()]
    all_hasLink = [db_hasLink.hasLink for db_hasLink in db.session.query(models.Messages).all()]
    all_imageLink = [db_imageLink.imageLink for db_imageLink in db.session.query(models.Messages).all()]
    all_hyperlink = [db_hyperlink.hyperlink for db_hyperlink in db.session.query(models.Messages).all()]
    
    messageObjects = []
    # Make a list of message objects, iterating through every list using an index.
    for i in range(len(all_messages)):
        currObject = {}
        currObject["message"] = all_messages[i]
        currObject["username"] = all_users[i]
        currObject["isBot"] = all_bot_status[i]
        currObject["profilePicture"] = all_profile_pictures[i]
        currObject["hasImage"] = all_hasImage[i]
        currObject["hasLink"] = all_hasLink[i]
        currObject["imageLink"] = all_imageLink[i]
        currObject["hyperlink"] = all_hyperlink[i]
        messageObjects.append(currObject)
    
    # Send each message using socketio to the client.
    socketio.emit('message dump', messageObjects)

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
        retObj = {
            "message": None,
            "isBot": True,
            "username": "Meerkat Bot",
            "profilePicture": "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/68083/meerkat-face-clipart-xl.png",
            "hasImage": False,
            "hasLink": False,
            "hyperlink": None,
            "imageLink": None
        }
        getBotResponse(retObj, messageContents)
    # If it's a user, either call their username from the dictionary above or create a username for them.
    else:
        splitMessage = messageContents.split()
        hasImage = False
        hasLink = False
        hyperlink = None
        imageLink = None
        
        for word in splitMessage:
            if "https://" in word or "http://" in word:
                if word[-3:] == "jpg" or word[-3:] == "png" or word[-3:] == "gif" or word[-4:] == "jpeg":
                    hasImage = True
                    imageLink = word
                else:
                    hasLink = True
                    hyperlink = word

        retObj["message"] = messageContents
        retObj["isBot"] = False
        retObj["username"] = usernameDict[flask.request.sid]["username"]
        retObj["profilePicture"] = usernameDict[flask.request.sid]["profilePicture"]
        retObj["hasImage"] = hasImage
        retObj["hasLink"] = hasLink
        retObj["hyperlink"] = hyperlink
        retObj["imageLink"] = imageLink
    
    # Write to the database the contents of the message, the username, and whether or not it's a bot message.
    db.session.add(models.Messages(\
        retObj['message'], \
        retObj['username'], \
        retObj['isBot'], \
        retObj['profilePicture'], \
        retObj['hasImage'], \
        retObj['hasLink'], \
        retObj["imageLink"], \
        retObj["hyperlink"]));

    db.session.commit()
    
    # Emit the message to socket.io
    socketio.emit('message recieved', retObj)

@socketio.on('user login')
def user_login(data):
    retObj = {}
    retObj["profilePicture"] = data["image"]
    retObj["username"] = "Meerkat Bot"
    retObj["message"] = data["name"] + " has joined the chat!"
    retObj["isBot"] = True
    
    db.session.add(models.Messages(\
    retObj['message'], \
    retObj['username'], \
    retObj['isBot'], \
    retObj['profilePicture'], \
    False, \
    False, \
    None, \
    None));
    db.session.commit()
    
    socketio.emit('message recieved', retObj)
    socketio.emit('unlock chat', {}, room=flask.request.sid)
    
    retObj["username"] = data["name"]
    retObj["isBot"] = False
    usernameDict[flask.request.sid] = retObj

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
