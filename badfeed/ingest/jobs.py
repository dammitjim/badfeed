from django_rq import job
from loguru import logger
import maya
import requests
from sentry_sdk import configure_scope

from badfeed.feeds.models import Feed
from badfeed.ingest.models import IngestLog
from badfeed.ingest.parser import RSSParser


@job
def sync_feed(feed: Feed):
    """Sync feed parsing against the database."""
    with configure_scope() as scope:
        logger.debug(f"Processing feed {feed.link}")
        scope.set_tag("feed", feed.title)

        r = requests.get(
            feed.link, headers={"User-Agent": "FeedBadger (tightenupthe.tech)"}
        )

        scope.set_extra("body", r.text)

        if r.status_code != 200:
            logger.error(
                f"{r.status_code} received when scraping {feed.link}", exc_info=True
            )
            IngestLog.objects.create(
                feed=feed, state=IngestLog.STATE_NOT_RESPONDING, body=r.text
            )
            return

        parser = RSSParser(feed)
        parser.parse(r)

        feed.date_last_scraped = maya.now().datetime()
        feed.save()
