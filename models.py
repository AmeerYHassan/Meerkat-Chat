# models.py
import flask_sqlalchemy
from app import db

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(750))
    username = db.Column(db.String(100))
    isBot = db.Column(db.Boolean())
    
    def __init__(self, a, b, c):
        self.message = a
        self.username = b
        self.isBot = c
        
    def __repr__(self):
        return '<Username: ' + self.username + ' Message: ' + self.message + 'isBot: ' + self.isBot + '>'