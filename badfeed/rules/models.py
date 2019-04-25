from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
import maya

from badfeed.feeds.models import Entry, EntryState, Feed


User = get_user_model()


class RuleManager(models.Manager):
    def active(self):
        """Filter for only active rules."""
        now = maya.now()
        return self.filter(date_start__gt=now, date_end__lt=now)


class Rule(models.Model):
    ACTION_CHOICES = [
        (EntryState.STATE_HIDDEN, "Hidden"),
        (EntryState.STATE_DELETED, "Deleted"),
    ]
    action = models.CharField(choices=ACTION_CHOICES, max_length=30)

    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rules")

    def match(self, entry) -> bool:
        """Verify that the entry matches the rule."""
        raise NotImplementedError("Rule must implement match function.")

    def apply(self, entry: Entry):
        """Apply the appropriate action to the entry based on the action saved to self."""
        if self.action == EntryState.STATE_DELETED:
            entry.mark_deleted(self.user)

    def save(self, **kwargs):
        """Ensure that the content type for the specific subclass is saved if not already."""
        if not self.content_type_id:
            self.content_type = ContentType.objects.get_for_model(self)
        return super().save(**kwargs)

    def specific(self):
        """Get the concrete subclass of the Rule to apply specific match functions against etc."""
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if isinstance(self, model_class) or model_class is None:
            return self
        return content_type.get_object_for_this_type(id=self.id)


class FeedRule(Rule):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_rules")

    def match(self, entry) -> bool:
        """The entry should share the same feed."""
        return self.feed == entry.feed


class TextMatchRule(Rule):
    text = models.CharField(max_length=100)

    def match(self, entry) -> bool:
        """The entry should contain the stated text."""
        entry_title = entry.title.lower()
        text_match_lower = self.text.lower()
        return text_match_lower in entry_title
