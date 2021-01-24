# setup for flask
import config
from flask import Flask

app = Flask(__name__)
app.debug = bool(config.DEBUG)


# setup for database
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
languages = wikipedia.languages()


# including other scripts
from src import views
