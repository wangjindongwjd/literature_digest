"""
translator.py

Translates English abstracts to Chinese using googletrans.
"""

import time
from googletrans import Translator


def translate_text(text: str, dest: str = "zh-cn") -> str:
    """Translate English text to Chinese using googletrans.

    Args:
        text: Input text to translate.
        dest: Target language code (default "zh-cn").

    Returns:
        Translated string, or original text on failure, or "" on empty input.
    """
    if not text:
        return ""

    # Limit input to first 5000 characters to avoid timeout
    truncated = text[:5000]

    try:
        translator = Translator()
        result = translator.translate(truncated, dest=dest)
        return result.text if result and result.text else truncated
    except Exception:
        return text


def translate_abstracts(papers: list[dict]) -> list[dict]:
    """Translate abstracts in a list of paper dicts and store in 'abstract_cn' field.

    Args:
        papers: List of paper dicts (as produced by pubmed_fetcher.fetch_details).

    Returns:
        The same list of dicts with an added 'abstract_cn' field on each.
    """
    for paper in papers:
        abstract = paper.get("abstract", "")
        if abstract:
            paper["abstract_cn"] = translate_text(abstract)
        else:
            paper["abstract_cn"] = ""
        time.sleep(0.3)  # avoid rate limiting

    return papers
