from django.contrib.autho.models import AbstractUser
from django.db import models

from badfeed.feeds.models import Feed


class BadFeedUser(AbstractUser):

    watching = models.ManyToManyField(Feed, related_name='watched_by')
