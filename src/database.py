from typing import Dict
from sqlalchemy import desc
from flask_sqlalchemy import BaseQuery

from src import db
from src.models import Users, Histories


def get_user(user_id: str) -> Users:
    """
    DBからLINEのユーザーIDに基づくユーザー情報を取得する

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        User: ユーザー情報
    """
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    if not user:
        user = Users()
        user.user_id = user_id
        db.session.add(user)
        db.session.commit()
    return user


def update_user(user_id: str, **kwargs: Dict) -> None:
    """
    ユーザー情報の更新

    Args:
        user_id(str): LINEのユーザーID
        kwargs: langかshow_urlをとる
    """
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
    """
    履歴の追加

    Args:
        user_id(str): LINEのユーザーID
        word(str): 検索結果のタイトル
    """
    history = Histories()
    history.user_id = user_id
    history.history = word
    db.session.add(history)
    db.session.commit()


def get_history(user_id: str) -> BaseQuery:
    """
    DBからLINEのユーザーIDに基づく検索履歴を最大13件取得する

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        BaseQuery: 履歴
    """
    return db.session.query(Histories).filter_by(user_id=user_id).order_by(desc(Histories.created_at)).limit(13)
