from src import app, handler, line_bot_api

import wikipedia
from flask import request, abort
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction)


def wikipedia_summary(input_text):
    msg = ''
    try:
        msg = wikipedia.summary(input_text).strip()
    except wikipedia.exceptions.PageError:
        msg = f'\"{input_text}\" は見つかりませんでした。'
    except wikipedia.exceptions.DisambiguationError:
        msg = '曖昧な単語が含まれています。'
    except wikipedia.exceptions.RedirectError:
        msg = 'ページタイトルが予期せずリダイレクトされました。'
    except wikipedia.exceptions.HTTPTimeoutError:
        msg = 'Mediawikiサーバーへのリクエストがタイムアウトしました。'
    finally:
        return msg


def wikipedia_search(input_text):
    items = wikipedia.search(input_text)
    items = [QuickReplyButton(action=MessageAction(label=i, text=i)) for i in items if len(i) <= 20][:13]
    return QuickReply(items=items) if items else None


@app.route('/', methods=['GET'])
def route():
    return 'ok'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    print(f'Received message: \'{message}\' from {user_name}')

    text = wikipedia_summary(message)
    quick_reply = wikipedia_search(message)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(
        text=text,
        quick_reply=quick_reply
    ))
