from src import app, handler, line_bot_api
from src.wiki import wikipedia_summary, wikipedia_search

from flask import request, abort
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)


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
