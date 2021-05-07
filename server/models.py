from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    active_time = db.Column(db.String(100))
    active= db.Column(db.String(100))
    last_time = db.Column(db.String(100))
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    post = db.Column(db.String(100))
    likes = db.Column(db.Integer)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.String(100), unique=True)
    history = db.Column(db.Text)
