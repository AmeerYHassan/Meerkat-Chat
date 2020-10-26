# models.py
# pylint: disable=C0114, C0103, C0115, R0902, E1101, R0913, R0903, W0611
# C0114, C0115 disabled since docstring is not necessary here
# C0103 disabled because modifying variable names now would conflict with the database
# R0902, R0913 disabled because each attribute is necessary
# E1101 states that SQLAlchemy is missing members, but it is a false positive
# W0611 states that flask_sqlalchemy is not used, but it is.
# R0903 states that too few public methods are created, but they are not necessary to be created

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
        return '<Username: ' + self.username + ' Message: ' + self.message + '>'
