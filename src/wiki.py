import wikipedia
from typing import Tuple, Union

from linebot.models import (QuickReply, QuickReplyButton, MessageAction)


def wikipedia_page(search_word: str, show_url: bool = False) -> Tuple[str, str]:
    title = ''
    text = ''
    try:
        page = wikipedia.page(search_word)
        title = page.title
        summary = page.summary.replace('\n', '')
        text = f'Result: {title}\n\n{summary}'
        if show_url:
            text += f'\n\n{page.url}'
    except wikipedia.exceptions.PageError:
        text = 'There was no match.'
    except wikipedia.exceptions.DisambiguationError:
        text = 'Contains ambiguous words.'
    except wikipedia.exceptions.RedirectError:
        text = 'The page title was unexpectedly redirected.'
    except wikipedia.exceptions.HTTPTimeoutError:
        text = 'The request to the Mediawiki server timed out.'
    finally:
        return title, text if text else 'none'


def wikipedia_search(search_word: str) -> Union[QuickReply, None]:
    if search_word:
        items = wikipedia.search(search_word, results=13)
        items = [QuickReplyButton(action=MessageAction(label=i if len(i) <= 20 else '{:.17}...'.format(i), text=i)) for i in items]
        return QuickReply(items=items) if items else None
    else:
        return None


def wikipedia_random(show_url: bool = False) -> Tuple[str, str]:
    word = wikipedia.random()
    return wikipedia_page(word, show_url=show_url)
