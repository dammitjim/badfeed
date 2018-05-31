from django.contrib.auth.models import AbstractUser
from django.db import models

from badfeed.feeds.models import Feed


class BadFeedUser(AbstractUser):

    email = models.EmailField(unique=True)
    watching = models.ManyToManyField(Feed, related_name="watched_by", blank=True)
