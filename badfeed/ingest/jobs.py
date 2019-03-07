import logging

from django_rq import job
import maya
import requests
from sentry_sdk import configure_scope

from badfeed.feeds.models import Feed
from badfeed.ingest.parser import RSSParser


log = logging.getLogger("rq.worker")


@job
def sync_feed(feed: Feed):
    """Sync feed parsing against the database."""
    with configure_scope() as scope:
        log.info(f"importing feed {feed.link}")
        scope.set_tag("feed", feed.title)

        r = requests.get(feed.link)

        scope.set_extra("body", r.text)

        if r.status_code != 200:
            # TODO: store failures as database objects
            log.error(
                f"{r.status_code} received when scraping {feed.link}", exc_info=True
            )
            return

        parser = RSSParser(feed)
        parser.parse(r)

        feed.date_last_scraped = maya.now()
        feed.save()
