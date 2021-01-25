from datetime import datetime

from src import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    lang = db.Column(db.String(80), default='ja')
    show_url = db.Column(db.Boolean, default=False)


class Histories(db.Model):
    __tablename__ = 'histories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    history = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.now)
