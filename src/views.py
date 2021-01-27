from flask import request, abort
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage)

from src import app, handler, line
from src.message import create_reply_content


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
    user_name = line.get_profile(user_id).display_name
    print(f'Received message: \'{message}\' from {user_name}')
    reply_content = create_reply_content(message, user_id)
    line.reply_message(event.reply_token, reply_content)
