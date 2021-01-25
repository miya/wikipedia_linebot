from sqlalchemy import desc

from src import db
from src.models import Users, Histories


def get_user(user_id):
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    if not user:
        user = Users()
        user.user_id = user_id
        db.session.add(user)
        db.session.commit()
    return user


def update_user(user_id, **kwargs):
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


def add_history(user_id, message):
    history = Histories()
    history.user_id = user_id
    history.history = message
    db.session.add(history)
    db.session.commit()


def get_history(user_id):
    return db.session.query(Histories)\
        .filter_by(user_id=user_id)\
        .order_by(desc(Histories.created_at))\
        .limit(13)
