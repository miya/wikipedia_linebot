from datetime import datetime

from src import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    lang = db.Column(db.String(80), default='ja')


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    history = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.now)
