from collections import namedtuple
from typing import List

from bleach import clean
from django.utils.text import Truncator
from feedparser import FeedParserDict

from badfeed.feeds.models import Feed, Tag

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


def get_or_create_tags(entry: FeedParserDict, feed: Feed) -> List[Tag]:
    """From the parsed entry and given feed, get or create tags from the database."""
    tags = []

    for tag in entry.tags:
        term = tag.term.lower()

        try:
            db_tag = Tag.objects.get(term=term, feed=feed)
        except Tag.DoesNotExist:
            db_tag = Tag(
                term=term,
                scheme=tag.get("scheme", ""),
                label=tag.get("label", ""),
                feed=feed,
            )
            db_tag.save()

        tags.append(db_tag)

    return tags
