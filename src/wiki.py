import wikipedia
from linebot.models import (QuickReply, QuickReplyButton, MessageAction)


def wikipedia_summary(input_text):
    msg = 'none'
    try:
        msg = wikipedia.summary(input_text).strip()
    except wikipedia.exceptions.PageError:
        msg = 'There was no match.'
    except wikipedia.exceptions.DisambiguationError:
        msg = 'Contains ambiguous words.'
    except wikipedia.exceptions.RedirectError:
        msg = 'The page title was unexpectedly redirected.'
    except wikipedia.exceptions.HTTPTimeoutError:
        msg = 'The request to the Mediawiki server timed out.'
    finally:
        return msg


def wikipedia_search(input_text):
    items = wikipedia.search(input_text, results=13)
    items = [QuickReplyButton(action=MessageAction(label=i if len(i) <= 20 else '{:.17}...'.format(i), text=i)) for i in items]
    return QuickReply(items=items) if items else None