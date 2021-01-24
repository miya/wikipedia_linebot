# setup for flask
import config
from flask import Flask

app = Flask(__name__)
app.debug = bool(config.DEBUG)


# setup for line-bot-sdk
from linebot import (LineBotApi, WebhookHandler)

LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# setup for wikipedia
import wikipedia
import warnings

warnings.simplefilter('ignore')
wikipedia.set_lang('ja')


# including other scripts
from src import controller
