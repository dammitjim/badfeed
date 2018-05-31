from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.exceptions import ParseError

from badfeed.feeds.models import Feed


class BadFeedUser(AbstractUser):

    email = models.EmailField(unique=True)
    watching = models.ManyToManyField(Feed, related_name="watched_by", blank=True)

    def watch(self, feed, commit=False):
        if self.watching.filter(pk=feed.pk).exists():
            raise ParseError("You are already watching this feed.")

        self.watching.add(feed)
        if commit:
            self.save()
