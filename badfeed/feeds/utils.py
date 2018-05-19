from collections import namedtuple

from bleach import clean
from django.utils.text import Truncator

CleanedContent = namedtuple("CleanedContent", ["teaser", "article"])


def clean_content(content):
    cleaned_full_content = clean(
        content,
        strip=True,
        tags=["b", "i", "a", "img", "p", "div"],
        attributes={"a": ["href", "title"], "img": ["src"]},
        styles=[],
    )

    cleaned_teaser_content = clean(content, strip=True)
    truncator = Truncator(cleaned_teaser_content)
    teaser = truncator.words(100)
    return CleanedContent(teaser=teaser.strip(), article=cleaned_full_content.strip())


def clean_item_content(item_content):
    content = ""
    for section in item_content:
        content += section.value
    return clean_content(content)
