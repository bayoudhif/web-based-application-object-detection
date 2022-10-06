from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    active=db.Column(db.Boolean(),default=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

    
class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.Integer)
    name = db.Column(db.String(1000))
    quantity = db.Column(db.Integer,default=5)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



