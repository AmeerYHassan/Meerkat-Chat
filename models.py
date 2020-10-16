# models.py
import flask_sqlalchemy
from app import db

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(750))
    username = db.Column(db.String(100))
    isBot = db.Column(db.Boolean())
    profilePicture = db.Column(db.String(750))
    hasImage = db.Column(db.Boolean())
    hasLink = db.Column(db.Boolean())
    imageLink = db.Column(db.String(750))
    hyperlink = db.Column(db.String(750))
    
    def __init__(self, a, b, c, d, e, f, g, h):
        self.message = a
        self.username = b
        self.isBot = c
        self.profilePicture = d
        self.hasImage = e
        self.hasLink = f
        self.imageLink = g
        self.hyperlink = h
        
    def __repr__(self):
        return '<Username: ' + self.username + ' Message: ' + self.message + 'isBot: ' + self.isBot + '>'