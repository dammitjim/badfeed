import logging

from dateutil import parser
from django.utils.timezone import now
from django_rq import job
from feedparser import parse

from .models import Entry
from .utils import clean_item_content, clean_content


log = logging.getLogger("rq.worker")


@job
def pull_feed(feed):
    log.info(f"importing feed {feed.url}")
    response = parse(feed.url)
    for entry in response.entries:
        if Entry.objects.filter(remote_id=entry.id, feed=feed).exists():
            log.debug(f"skipping {entry.link}")
            continue

        log.info(f"pulling {entry.link}")

        date_published = parser.parse(entry.published)

        if hasattr(entry, "content"):
            content = clean_item_content(entry.content)
        elif hasattr(entry, "description"):
            content = clean_content(entry.description)
        else:
            log.error(f"could not find parsable content for {entry.id}")
            continue
        teaser = entry.description if hasattr(entry, "description") else content.teaser

        db_entry = Entry(
            name=entry.title,
            url=entry.link,
            date_first_published=date_published,
            teaser=teaser,
            feed=feed,
            remote_id=entry.id,
            content=content.article,
        )

        try:
            db_entry.full_clean()
            db_entry.save()
        except Exception as e:
            log.exception(f"failed to create entry for {entry.link}", exc_info=e)
    feed.date_last_scraped = now()
    feed.save()
