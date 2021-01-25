from sqlalchemy import desc
from typing import Dict
from flask_sqlalchemy import BaseQuery

from src import db
from src.models import Users, Histories


def get_user(user_id: str) -> Users:
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    if not user:
        user = Users()
        user.user_id = user_id
        db.session.add(user)
        db.session.commit()
    return user


def update_user(user_id: str, **kwargs: Dict) -> None:
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    if not user:
        user = Users()
        user.user_id = user_id
        if kwargs.get('lang'):
            user.lang = kwargs['lang']
        if kwargs.get('show_url') is not None:
            user.show_url = kwargs['show_url']
        db.session.add(user)
        db.session.commit()
    else:
        if kwargs.get('lang'):
            user.lang = kwargs['lang']
        if kwargs.get('show_url') is not None:
            user.show_url = kwargs['show_url']
        db.session.add(user)
        db.session.commit()


def add_history(user_id: str, word: str) -> None:
    history = Histories()
    history.user_id = user_id
    history.history = word
    db.session.add(history)
    db.session.commit()


def get_history(user_id: str) -> BaseQuery:
    return db.session.query(Histories)\
        .filter_by(user_id=user_id)\
        .order_by(desc(Histories.created_at))\
        .limit(13)
