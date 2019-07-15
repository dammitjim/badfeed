from django.conf import settings
from django.core.management.base import BaseCommand

from feedzero.feeds.models import Feed
from feedzero.ingest.jobs import sync_feed


class Command(BaseCommand):
    help = "Enqueue feeds to be parsed"

    def add_arguments(self, parser):
        # TODO: pass in specific feeds
        pass

    def handle(self, *args, **options):
        # TODO: limit to ones due for update when development is further
        for feed in Feed.objects.filter(scraping_enabled=True):
            if settings.RQ_ENABLED:
                sync_feed.delay(feed)
            else:
                sync_feed(feed)
