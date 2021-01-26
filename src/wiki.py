import wikipedia
from typing import List, Tuple


def wikipedia_page(search_word: str, show_url: bool = False) -> Tuple[str, str, List]:
    """
    search_wordをWikipediaで検索する

    Args:
        search_word(str): 検索ワード
        show_url(bool): 要約テキストにURLを含めるかどうか

    Returns:
        title(str): 検索結果のタイトル
        text(str): 検索結果の要約
        candidates(list): 検索結果が存在する場合は空のリスト、検索結果が存在しない場合は候補タイトル
    """
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
    except wikipedia.exceptions.RedirectError:
        text = 'The page title was unexpectedly redirected'
    except wikipedia.exceptions.HTTPTimeoutError:
        text = 'The request to the Mediawiki server timed out'
    return title, text, candidates


def wikipedia_search(search_word: str) -> List:
    """
    search_wordでWikipediaの関連タイトルを取得する

    Args:
        search_word(str): 検索ワード

    Returns:
        list: 関連ワード
    """
    return wikipedia.search(search_word, results=13)


def wikipedia_random(show_url: bool = False) -> Tuple[str, str, List]:
    """
    Wikipediaでランダムなタイトルを取得しwikipedia_page関数に渡す

    Args:
        show_url(bool): 要約テキストにURLを含めるかどうか

    Returns:
        title(str): 検索結果のタイトル
        text(str): 検索結果の要約
        candidates(list): 検索結果が存在する場合は空のリスト、検索結果が存在しない場合は候補タイトル
    """
    return wikipedia_page(search_word=wikipedia.random(), show_url=show_url)
