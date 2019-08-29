from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from feedzero.feeds.jobs import enrich_feed_with_favicon
from feedzero.feeds.models import Feed


@receiver(post_save, sender=Feed, dispatch_uid="queue_logo_fetch")
def queue_logo_fetch(sender, instance, created):
    if created or not instance.logo:
        if settings.RQ_ENABLED:
            enrich_feed_with_favicon.delay(instance)
        else:
            enrich_feed_with_favicon(instance)
