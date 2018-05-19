from django.core.management.base import BaseCommand
from django.conf import settings

from badfeed.feeds.models import Feed
from badfeed.feeds.jobs import pull_feed


class Command(BaseCommand):
    help = "Enqueue feeds to be parsed"

    def add_arguments(self, parser):
        # TODO: pass in specific feeds
        pass

    def handle(self, *args, **options):
        # TODO: limit to ones due for update when development is further
        for feed in Feed.objects.all():
            if settings.RQ_ENABLED:
                pull_feed.delay(feed)
            else:
                pull_feed(feed)
