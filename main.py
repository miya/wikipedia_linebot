import os
import warnings
import wikipedia
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)


# Flaskのインスタンス
app = Flask(__name__)

# wikipediaの言語設定
wikipedia.set_lang('ja')

# 警告の無視
warnings.simplefilter('ignore')

# アクセストークンの設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def wiki(input_text):
    msg = ''
    try:
        msg = wikipedia.summary(input_text)
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

    result = wiki(message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))


if __name__ == '__main__':
    app.run(threaded=True)
