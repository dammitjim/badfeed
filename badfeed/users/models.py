from django.contrib.auth.models import AbstractUser
from django.db import models

from badfeed.feeds.models import Feed


class BadFeedUser(AbstractUser):

    email = models.EmailField(unique=True)
    watching = models.ManyToManyField(Feed, related_name="watched_by", blank=True)

    def watch(self, feed, commit=False):
        if self.watching.filter(pk=feed.pk).exists():
            raise ValueError("You are already watching this feed.")

        self.watching.add(feed)
        if commit:
            self.save()

    def unwatch(self, feed, commit=False):
        if not self.watching.filter(pk=feed.pk).exists():
            raise ValueError("You are not watching this feed")

        self.watching.remove(feed)
        if commit:
            self.save()
