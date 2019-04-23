from django.contrib.auth import get_user_model
from django.db import models

from badfeed.feeds.models import EntryState, Feed


User = get_user_model()


class Rule(models.Model):
    ACTION_CHOICES = [
        (EntryState.STATE_HIDDEN, "Hidden"),
        (EntryState.STATE_DELETED, "Deleted"),
    ]
    action = models.CharField(choices=ACTION_CHOICES, max_length=30)

    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rules")


class FeedRule(Rule):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_rules")


class TextMatchRule(Rule):
    text = models.CharField(max_length=100)
