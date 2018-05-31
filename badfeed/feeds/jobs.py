import logging

from dateutil import parser
from django_rq import job
from django.utils import timezone
import feedparser

from badfeed.feeds.exceptions import ContentErrorException
from badfeed.feeds.models import Entry, Enclosure, Tag, Author
from badfeed.feeds.utils import clean_item_content, clean_content


log = logging.getLogger("rq.worker")


class EntryIngest:
    def __init__(self, feed):
        self.feed = feed
        self._ingest_entry = None

    def get_date_published(self):
        return parser.parse(self._ingest_entry.published)

    def get_content(self):
        if hasattr(self._ingest_entry, "content"):
            return clean_item_content(self._ingest_entry.content).article

        if hasattr(self._ingest_entry, "description"):
            return clean_content(self._ingest_entry.description).article

        raise ContentErrorException("no content")

    def get_summary(self):
        # TODO: the summary needs to strip all html tags i think
        if hasattr(self._ingest_entry, "summary_detail"):
            return clean_content(self._ingest_entry.summary_detail.value).article

        if hasattr(self._ingest_entry, "summary"):
            return clean_content(self._ingest_entry.summary).article

        return ""

    def get_guid(self):
        if not hasattr(self._ingest_entry, "id"):
            raise ValueError("no guid present on ingest entry")

        return self._ingest_entry.id

    def get_title(self):
        if not hasattr(self._ingest_entry, "title"):
            raise ValueError("no title present on ingest entry")

        return self._ingest_entry.title

    def get_link(self):
        if not hasattr(self._ingest_entry, "link"):
            raise ValueError("no link present on ingest entry")

        return self._ingest_entry.link

    def get_author(self, commit=True):
        # TODO: some feeds have comma separated author fields, check if a comma is present and split on it
        if hasattr(self._ingest_entry, "author_detail"):
            try:
                db_author = Author.objects.get(name=self._ingest_entry.author_detail.name, feed=self.feed)
            except Author.DoesNotExist:
                db_author = Author(
                    name=self._ingest_entry.author_detail.name,
                    link=self._ingest_entry.author_detail.get("link", ""),
                    email=self._ingest_entry.author_detail.get("email", ""),
                    feed=self.feed,
                )
                if commit:
                    db_author.save()
            return db_author

        if hasattr(self._ingest_entry, "author"):
            try:
                db_author = Author.objects.get(name=self._ingest_entry.author, feed=self.feed)
            except Author.DoesNotExist:
                db_author = Author(name=self._ingest_entry.author, feed=self.feed)
                if commit:
                    db_author.save()
            return db_author

        return None

    def get_contributors(self, commit=True):
        if not hasattr(self._ingest_entry, "contributors"):
            return None

        contributors = []
        for contributor in self._ingest_entry.contributors:
            try:
                db_author = Author.objects.get(name=contributor.name, feed=self.feed)
            except Author.DoesNotExist:
                db_author = Author(
                    name=contributor.name,
                    link=contributor.get("href", ""),
                    email=contributor.get("email", ""),
                    feed=self.feed,
                )
                if commit:
                    db_author.save()
            contributors.append(db_author)
        return contributors

    def get_tags(self, commit=True):
        if not hasattr(self._ingest_entry, "tags"):
            return None

        tags = []
        for tag in self._ingest_entry.tags:
            term = tag.term.lower()
            try:
                db_tag = Tag.objects.get(term=term, feed=self.feed)
            except Tag.DoesNotExist:
                db_tag = Tag(term=term, scheme=tag.get("scheme", ""), label=tag.get("label", ""), feed=self.feed)
                if commit:
                    db_tag.save()
            tags.append(db_tag)
        return tags

    def get_enclosures(self, entry, commit=True):
        if not hasattr(self._ingest_entry, "enclosures"):
            return None

        enclosures = [
            Enclosure(href=enclosure.href, length=enclosure.length, file_type=enclosure.type, entry=entry)
            for enclosure in self._ingest_entry.enclosures
        ]

        if commit:
            for enclosure in enclosures:
                enclosure.save()

        return enclosures

    def ingest(self, ingest_entry, commit=True):
        self._ingest_entry = ingest_entry

        entry = Entry(
            title=self.get_title(),
            link=self.get_link(),
            date_published=self.get_date_published(),
            content=self.get_content(),
            summary=self.get_summary(),
            guid=self.get_guid(),
            feed=self.feed,
            author=self.get_author(commit=commit),
        )
        entry.full_clean()

        if commit:
            entry.save()

        self.get_enclosures(entry, commit=commit)

        tags = self.get_tags(commit=commit)
        if tags:
            entry.tags.add(*tags)

        contributors = self.get_contributors(commit=commit)
        if contributors:
            entry.contributors.add(*contributors)

        if (tags or contributors) and commit:
            entry.save()

        return entry


@job
def pull_feed(feed, save=True):
    log.info(f"importing feed {feed.link}")
    response = feedparser.parse(feed.link)
    for entry in response.entries:
        if Entry.objects.filter(guid=entry.id, feed=feed).exists() and save:
            log.debug(f"skipping {entry.link}")
            continue

        log.info(f"pulling {entry.link}")
        EntryIngest(feed).ingest(entry, commit=save)

    if not save:
        return

    feed.date_last_scraped = timezone.now()
    feed.save()
