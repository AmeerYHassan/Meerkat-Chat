# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import requests
import os
import flask
import flask_sqlalchemy
import flask_socketio
import requests
import random

animals = ["Cat", "Dog", "Elephant", "Serval", "Ocelot", "Giraffe", "Bear", "Panda", "Bird", "Lizard", "Skink", "Fish"]
adjectives = ["Enjoyable", "Astonishing", "Super", "Amusing", "Large", "Fancy", "Kind", "Delightful", "Eager", "Bright", "Amiable", "Generous"]
takenNames = set()
usernameDict = {}

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

import models 

def getBotResponse(message):
    splitMessage = message.split()
    messageResponse = ""
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
    elif "catfact" in splitMessage[0]:
        response = requests.get("https://catfact.ninja/fact")
        if (response.status_code == 200):
            messageResponse = response.json()["fact"]
        else:
            messageResponse = "Uh oh! Try again in a few, I can't seem to get a cat fact right now."
    elif "time" in splitMessage[0]:
        messageResponse = "The current time is " + datetime.now().strftime("%H:%M:%S")
    elif "about" in splitMessage[0]:
        messageResponse = "Hi, I'm meerkat, and I'm just a small utility for this chat room! Use !!help to see what I can do!"
    elif "help" in splitMessage[0]:
        messageResponse = "!!funtranslate <message> to translate a message to yoda speech, !!time to get the current time, !!catfact to get a random cat fact, or !!about to learn a bit more about me"
    else:
        messageResponse = "Sorry, I don't know that command. Use !!help to see what I can do!"
    
    return messageResponse

@socketio.on('connect')
def on_connect():
    socketio.emit('user count change', { "changeBy": +1 })
    print("A user has connected")

@socketio.on('disconnect')
def on_disconnect():
    socketio.emit('user count change', { "changeBy": -1 })
    print("A user has disconnected")
    
@socketio.on('new message')
def new_message(data):
    messageContents = data["message"]
    retObj = {}
    if (messageContents[0:2] == "!!"):
        retObj["message"] = getBotResponse(messageContents)
        retObj["isBot"] = True
        retObj["username"] = "Meerkat Bot"
    else:
        retObj["message"] = messageContents
        retObj["isBot"] = False
        if (flask.request.sid in usernameDict):
            retObj["username"] = usernameDict[flask.request.sid]
        else:
            newUser = random.choice(adjectives) + " " + random.choice(animals) + " " + str(random.randint(1, 100))
            while newUser in takenNames:
                newUser = random.choice(adjectives) + " " + random.choice(animals) + " " + str(random.randint(1, 100))
            takenNames.add(newUser)
            usernameDict[flask.request.sid] = newUser
            retObj["username"] = usernameDict[flask.request.sid]
                
    socketio.emit('message recieved', retObj)
    print(flask.request.sid)
    print(retObj)
    print(messageContents)
    print(data)

@app.route('/')
def index():
    return flask.render_template("index.html")
    
    
if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
