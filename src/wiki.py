import wikipedia
from linebot.models import (QuickReply, QuickReplyButton, MessageAction)


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
    items = wikipedia.search(input_text, results=13)
    items = [QuickReplyButton(action=MessageAction(label=i, text=i)) for i in items if len(i) <= 20]
    return QuickReply(items=items) if items else None