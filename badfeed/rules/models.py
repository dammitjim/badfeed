from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
import maya

from badfeed.feeds.models import Entry, EntryState, Feed


User = get_user_model()


class RuleManager(models.Manager):
    def active(self):
        """Filter for only active rules."""
        now = maya.now().datetime()
        return self.filter(
            Q(date_start__lte=now), Q(date_end__gte=now) | Q(date_end__isnull=True)
        )


class Rule(models.Model):
    """Base rule model, used to configure logic for user automation of entry processing."""

    ACTION_CHOICES = [
        (EntryState.STATE_HIDDEN, "Hidden"),
        (EntryState.STATE_DELETED, "Deleted"),
    ]
    action = models.CharField(choices=ACTION_CHOICES, max_length=30)

    date_start = models.DateTimeField(default=maya.now().datetime())
    date_end = models.DateTimeField(blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rules")

    objects = RuleManager()

    def match(self, entry: Entry) -> bool:
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

    @cached_property
    def specific(self):
        """Get the concrete subclass of the Rule to apply specific match functions against etc."""
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if isinstance(self, model_class) or model_class is None:
            return self
        return content_type.get_object_for_this_type(id=self.id)


class FeedRule(Rule):
    """Direct match against feed Rule."""

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_rules")

    def match(self, entry: Entry) -> bool:
        """The entry should share the same feed."""
        return self.feed == entry.feed


class TextMatchRule(Rule):
    """Naive 'does the entry title contain' level text match rule."""

    text = models.CharField(max_length=100)

    def match(self, entry: Entry) -> bool:
        """The entry should contain the stated text."""
        entry_title = entry.title.lower()
        text_match_lower = self.text.lower()
        return text_match_lower in entry_title
