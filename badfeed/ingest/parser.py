import logging
from typing import List

import feedparser
import maya
import requests

from badfeed.feeds.models import Entry, Feed
from badfeed.ingest.exceptions import ContentErrorException
from badfeed.ingest.utils import clean_content, get_or_create_tags


log = logging.getLogger("rq.worker")


class EntryParser:
    """Parse an individual entry."""

    clean_fn = clean_content

    def __init__(self, entry_data: feedparser.FeedParserDict):
        """Load initial entry data into the parser."""
        self.entry_data = entry_data

    def load(self, entry_data):
        """Load the given entry data into the parser, replacing the existing."""
        self.entry_data = entry_data

    def extract(self) -> dict:
        """Extract the appropriate values from the entry_data."""
        data = {
            "title": self.entry_data.title,
            "link": self.entry_data.link,
            "guid": self.entry_data.id,
        }

        data["date_published"] = maya.parse(self.entry_data.published).datetime()
        data["content"] = self._get_content()
        data["summary"] = self._get_summary()

        return data

    def _get_content(self) -> str:
        """Get the data for the content field of the Entry."""
        field = None
        if hasattr(self.entry_data, "content"):
            field = self.entry_data.content
        elif hasattr(self.entry_data, "description"):
            field = self.entry_data.description
        else:
            raise ContentErrorException("content")

        return self._clean(field)

    def _get_summary(self) -> str:
        """Get the data for the summary field of the Entry."""
        field = None
        if hasattr(self.entry_data, "summary_detail"):
            field = self.entry_data.content
        elif hasattr(self.entry_data, "summary"):
            field = self.entry_data.description
        else:
            raise ContentErrorException("content")

        return self._clean(field)

    def _clean(self, text_value) -> str:
        cleaned = self.clean_fn(text_value)
        return cleaned.article


class RSSParser:
    def __init__(self, feed: Feed):
        """Initialise feed as a constant (lol constants in python)."""
        self.FEED = feed

    def get_entries_to_process(self, entries: List[feedparser.FeedParserDict]):
        """Yield entries which don't currently exist.

        Could potentially instead return a list comp. Think this uses less memory.
        TODO we need to be able to update existing entries?
        """
        for entry in entries:
            if not Entry.objects.filter(guid=entry.id, feed=self.FEED).exists():
                yield entry

    def parse(self, response: requests.Response):
        """Parse the RSS feed response into the database.

        TODO in future take example responses and patch the `response.text` in tests
        """
        entry_parser = None
        data = feedparser.parse(response.text)

        for entry in self.get_entries_to_process(data.entries):
            try:
                if not entry_parser:
                    entry_parser = EntryParser(entry)
                else:
                    entry_parser.load(entry)

                entry_extract = entry_parser.extract()

                db_entry = Entry(feed=self.FEED, **entry_extract)
                db_entry.full_clean()
                db_entry.save()

                tags = get_or_create_tags(entry, self.FEED)
                if len(tags) > 0:
                    db_entry.tags.add(*tags)
                    db_entry.save()

            except Exception:
                log.exception("Failed to parse entry.", exc_info=True)
                continue
                # TODO save failed data to file or something here
