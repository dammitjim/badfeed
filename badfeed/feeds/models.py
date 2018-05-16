from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from badfeed.core.models import Slugified
# from .models import User


class Feed(Slugified, models.Model):
    """A feed of content."""
    slugify_source = 'name'

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1000, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_last_scraped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Entry(Slugified, models.Model):
    """An entry into a Feed."""
    slugify_source = 'name'

    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    remote_id = models.CharField(max_length=1000)

    content = models.TextField()
    teaser = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_first_published = models.DateTimeField(blank=True, null=True)

    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    def get_additional_slug_filters(self):
        """Used by Slugified to help generate the slug by uniqueness."""
        return {'feed': self.feed}

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'entries'
        unique_together = (('remote_id', 'feed'), )


class Media(models.Model):
    """A media file, often contained within an enclosure."""
    url = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = 'media'


# class EntryState(models.Model):
#     """Track the entry state in relation to the user, can be saved or archived."""
#     STATE_SAVED = 'saved'
#     STATE_ARCHIVED = 'archived'
#     STATE_NA = 'na'
#     STATE_CHOICES = (
#         (STATE_SAVED, 'Saved'),
#         (STATE_ARCHIVED, 'Archived'),
#         (STATE_NA, 'N/A')
#     )
#     state = models.CharField(max_length=255, choices=STATE_CHOICES, default=STATE_NA)
#     viewed = models.BooleanField(default=False)
#     date_updated = models.DateTimeField(auto_now_add=True)

#     entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='entry_state')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_state')
