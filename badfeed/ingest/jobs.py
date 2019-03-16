from django_rq import job
import maya
import requests
from sentry_sdk import configure_scope
from loguru import logger

from badfeed.feeds.models import Feed
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
            # TODO: store failures as database objects
            logger.error(
                f"{r.status_code} received when scraping {feed.link}", exc_info=True
            )
            return

        parser = RSSParser(feed)
        parser.parse(r)

        feed.date_last_scraped = maya.now().datetime()
        feed.save()
