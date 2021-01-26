import wikipedia
from typing import List, Tuple


def wikipedia_page(search_word: str, show_url: bool = False) -> Tuple[str, str, List]:
    title = ''
    candidates = []
    try:
        page = wikipedia.page(search_word)
        title = page.title
        summary = page.summary.replace('\n', '')
        text = f'Result: {title}\n\n{summary}'
        if show_url:
            text += f'\n\n{page.url}'
    except wikipedia.exceptions.PageError:
        text = 'There was no match'
    except wikipedia.exceptions.DisambiguationError as e:
        text = f'Contains ambiguous words -> "{search_word}"'
        candidates = e.options
        print(candidates)
    except wikipedia.exceptions.RedirectError:
        text = 'The page title was unexpectedly redirected'
    except wikipedia.exceptions.HTTPTimeoutError:
        text = 'The request to the Mediawiki server timed out'
    return title, text, candidates


def wikipedia_search(search_word: str) -> List:
    return wikipedia.search(search_word, results=13)


def wikipedia_random(show_url: bool = False) -> Tuple[str, str, List]:
    return wikipedia_page(search_word=wikipedia.random(), show_url=show_url)
