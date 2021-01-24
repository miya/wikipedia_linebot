from sqlalchemy import desc

from src import db
from src.models import User, History


def get_user(user_id):
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User()
        user.user_id = user_id
        db.session.add(user)
        db.session.commit()
    return user


def update_lang(user_id, lang):
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User()
        user.user_id = user_id
        user.lang = lang
        db.session.add(user)
        db.session.commit()
    else:
        user.lang = lang
        db.session.add(user)
        db.session.commit()


def add_history(user_id, message):
    history = History()
    history.user_id = user_id
    history.history = message
    db.session.add(history)
    db.session.commit()


def get_history(user_id):
    return db.session.query(History)\
        .filter_by(user_id=user_id)\
        .order_by(desc(History.created_at))\
        .limit(13)
