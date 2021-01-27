import re
import wikipedia
from typing import List, Union
from linebot.models import (TextSendMessage, QuickReply, QuickReplyButton, MessageAction)

from src import languages
from src.wiki import wikipedia_page, wikipedia_search, wikipedia_random
from src.database import get_user, update_user, get_history, add_history


def create_quick_reply(items: List) -> Union[QuickReply, None]:
    """
    itemsからQuickReplyを生成

    Args:
        items(list): wikipediaで検索するタイトル

    Returns:
        QuickReply or None: itemsに値が入っていた場合はQuickReply、空だった場合はNone
    """
    qr_items = [
        QuickReplyButton(
            action=MessageAction(label=i if len(i) <= 20 else '{:.17}...'.format(i), text=i)) for i in items[:13]
    ]
    return QuickReply(items=qr_items) if qr_items else None


def create_reply_content(message: str, user_id: str) -> TextSendMessage:
    """
    クライアントから受け取ったメッセージから返信メッセージを生成する

    Args:
        message(str): クライアントが送信したメッセージ
        user_id(str): LINEのユーザーID

    Returns:
        TextSendMessage
    """

    # 履歴
    if message == ':history':
        reply_content = history_message(user_id)

    # ランダム
    elif message == ':random':
        reply_content = random_message(user_id)

    # 言語設定
    elif ':set_lang' in message:
        reply_content = set_lang(user_id, message)

    # URLを含めるか設定
    elif ':set_show_url' in message:
        print('え')
        reply_content = set_show_url(user_id, message)

    # 受け取ったメッセージで検索
    else:
        reply_content = summary_message(user_id, message)

    return reply_content


def history_message(user_id: str) -> TextSendMessage:
    """
    user_idに基づく最大13個の検索履歴を返す

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        TextSendMessage
    """
    history = get_history(user_id)
    text = '--- History ---\n\n'
    items = []
    for h in history:
        text += f'・{h.history}\n'
        items.append(h.history)
    quick_reply = create_quick_reply(items)
    return TextSendMessage(text=text.rstrip() if text else 'No history yet', quick_reply=quick_reply)


def random_message(user_id: str) -> TextSendMessage:
    """
    Wikipediaのランダムなタイトルで検索

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        TextSendMessage
    """
    user = get_user(user_id)
    wikipedia.set_lang(user.lang)
    random = wikipedia_random(show_url=user.show_url)
    title = random[0]
    text = random[1]
    candidates = random[2]
    if title:
        add_history(user_id, title)
        items = wikipedia_search(title)
        quick_reply = create_quick_reply(items)
    else:
        quick_reply = create_quick_reply(candidates)
        text += '\n\n'
        for c in candidates:
            text += f'・{c}\n'
        text = text.rstrip()
    return TextSendMessage(text=text, quick_reply=quick_reply)


def set_lang(user_id: str, message: str) -> TextSendMessage:
    """
    ユーザーの言語情報を更新します

    Args:
        user_id(str): LINEのユーザーID
        message(str): クライアントが送信したメッセージ

    Returns:
        TextSendMessage
    """
    user = get_user(user_id)
    text = 'Please enter the language code that exists'
    if message in [f':set_lang={lang}' for lang in languages.keys()]:
        lang = re.findall(':set_lang=(.+)', message)[0]
        if user.lang == lang:
            text = f'It is already set to "{languages[lang]}"'
        else:
            text = f'Changed the language setting to "{languages[lang]}"'
            update_user(user_id, lang=lang)
    return TextSendMessage(text=text)


def set_show_url(user_id: str, message: str) -> TextSendMessage:
    """
    ユーザーの要約メッセージにURLを含めるかの設定を行います

    Args:
        user_id(str): LINEのユーザーID
        message: クライアントが送信したメッセージ

    Returns:
        TextSendMessage
    """
    user = get_user(user_id)
    text = 'Please enter :show_url=true or :show_url=false'
    if message == ':set_show_url=true':
        if user.show_url:
            text = 'The show_url is already set to true'
        else:
            update_user(user_id, show_url=True)
            text = 'show_url is set to true'
    elif message == ':set_show_url=false':
        if not user.show_url:
            text = 'The show_url is already set to false'
        else:
            update_user(user_id, show_url=False)
            text = 'show_url is set to false'
    return TextSendMessage(text=text)


def summary_message(user_id: str, message: str) -> TextSendMessage:
    """
    メッセージに基づくWikipediaの要約メッセージを生成する

    Args:
        user_id(str): LINEのユーザーID
        message(srt): クライアントが送信したメッセージ

    Returns:
        TextSendMessage
    """
    user = get_user(user_id)
    wikipedia.set_lang(user.lang)
    page = wikipedia_page(message, show_url=user.show_url)
    title = page[0]
    text = page[1]
    candidates = page[2]
    if title:
        add_history(user_id, title)
        items = wikipedia_search(title)
        quick_reply = create_quick_reply(items)
    else:
        quick_reply = create_quick_reply(candidates)
        text += '\n\n'
        for c in candidates:
            text += f'・{c}\n'
        text = text.rstrip()
    return TextSendMessage(text=text, quick_reply=quick_reply)
