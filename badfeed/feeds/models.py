from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.text import Truncator
from loguru import logger
import maya

from badfeed.core.models import SlugifiedMixin


class FeedManager(models.Manager):
    """Custom manager for feed model, adds utility methods."""

    def watched_by(self, user):
        """Return feeds watched by the given user."""
        return self.filter(watched_by=user)


class Feed(SlugifiedMixin, models.Model):
    """A feed of content."""

    title = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, unique=True)

    scraping_enabled = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_last_scraped = models.DateTimeField(blank=True, null=True)

    objects = FeedManager()

    def __str__(self):
        """Str representation of feed."""
        return self.title

    @staticmethod
    def slug_uniqueness_check(text, uids):
        """Check for other feeds with this slug."""
        if text in uids:
            return False
        return not Feed.objects.filter(slug=text).exists()

    def is_watched_by(self, user) -> bool:
        """Assert user is contained within watched_by m2m field."""
        return user in self.watched_by.all()

    def mark_entries_archived(self, user):
        """Will archive all current unread entries."""
        entries = self.entries.all().exclude(states__isnull=False, states__user=user)
        # TODO this may be expensive, consider a bulk operation?
        for entry in entries:
            entry.mark_deleted(user)


class Author(models.Model):
    """An author of an entry."""

    name = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="authors")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """A tag to categories entries."""

    term = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=1000, blank=True, null=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        """Str representation of tag."""
        return self.term


class EntryUserStateManager(models.Manager):
    def unread(self, user):
        """Get all entries that haven't been read by the user yet."""
        feeds = Feed.objects.watched_by(user)
        entries = self.filter(feed__in=feeds).exclude(
            states__isnull=False, states__user=user
        )
        return entries.order_by("-date_published")

    def saved(self, user):
        """Get all entries that have been saved."""
        return self.filter(states__state=EntryState.STATE_SAVED, states__user=user)

    def pinned(self, user):
        """Get all entries that have been pinned."""
        return self.filter(states__state=EntryState.STATE_PINNED, states__user=user)

    def deleted(self, user):
        """Get all entries that have been deleted."""
        return self.filter(states__state=EntryState.STATE_DELETED, states__user=user)


class Entry(SlugifiedMixin, models.Model):
    """An entry into a Feed."""

    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    guid = models.CharField(max_length=1000)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)

    date_published = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="entries")

    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, blank=True, null=True, related_name="entries"
    )
    contributors = models.ManyToManyField(
        Author, related_name="contributed_to", blank=True
    )

    tags = models.ManyToManyField(Tag, related_name="entries", blank=True)

    objects = models.Manager()
    user_state = EntryUserStateManager()

    def get_initial_slug_uids(self):
        """Prepopulate slug uids with titles for entries in this feed.

        This is required due to the `unique_together` constraint of the model.
        """
        return [
            entry.title for entry in Entry.objects.filter(feed=self.feed).only("title")
        ]

    @staticmethod
    def slug_uniqueness_check(text, uids) -> bool:
        """Ensure no other entries with this slug exist."""
        if text in uids:
            return False
        return not Entry.objects.filter(slug=text).exists()

    def archive_older_than_this(self, user):
        """Mark all entries older than this entry, for this feed, as archived."""
        older_entries = Entry.objects.filter(
            date_created__lt=self.date_created, feed=self.feed
        )
        for entry in older_entries:
            entry.mark_deleted(user)

    def mark_read_by(self, user):
        """Create an entrystate object marking this entry as having been read."""
        return EntryState.objects.get_or_create(
            state=EntryState.STATE_READ, entry=self, user=user
        )

    def mark_pinned(self, user):
        """Pin the entry for the user if not already pinned."""
        return EntryState.objects.get_or_create(
            state=EntryState.STATE_PINNED, entry=self, user=user
        )

    def mark_unpinned(self, user):
        """Unpin the entry for the user."""
        try:
            state = EntryState.objects.get(
                state=EntryState.STATE_PINNED, entry=self, user=user
            )
            state.delete()
        except EntryState.DoesNotExist as e:
            logger.exception("Attempted to unpin an unpinned entry.", exc_info=e)

    def mark_deleted(self, user):
        """Pin the entry for the user if not already deleted.

        By marking for deletion, we also delete all other states.
        TODO consider moving this to the entry state model?
        """
        EntryState.objects.filter(entry=self, user=user).filter(
            Q(state=EntryState.STATE_PINNED) | Q(state=EntryState.STATE_SAVED)
        ).delete()
        return EntryState.objects.get_or_create(
            state=EntryState.STATE_DELETED, entry=self, user=user
        )

    def mark_undeleted(self, user):
        """Undelete the entry for the user."""
        try:
            state = EntryState.objects.get(
                state=EntryState.STATE_DELETED, entry=self, user=user
            )
            state.delete()
        except EntryState.DoesNotExist as e:
            logger.exception("Attempted to undelete an undeleted entry.", exc_info=e)

    def mark_saved(self, user):
        """Save the entry for the user if not already saved.

        If the entry has been pinned, delete the pin state.
        TODO consider moving this to the entry state model?
        """
        if self.is_pinned_by(user):
            EntryState.objects.filter(
                state=EntryState.STATE_PINNED, entry=self, user=user
            ).delete()
        return EntryState.objects.get_or_create(
            state=EntryState.STATE_SAVED, entry=self, user=user
        )

    def mark_unsaved(self, user):
        """Remove the saved state of an entry."""
        try:
            state = EntryState.objects.get(
                state=EntryState.STATE_SAVED, entry=self, user=user
            )
            state.delete()
        except EntryState.DoesNotExist as e:
            logger.exception("Attempted to undelete an undeleted entry.", exc_info=e)

    def is_pinned_by(self, user) -> bool:
        """Check if the given entry has been pinned by the given user."""
        return EntryState.objects.filter(
            state=EntryState.STATE_PINNED, entry=self, user=user
        ).exists()

    def is_saved_by(self, user) -> bool:
        """Check if the given entry has been saved by the given user."""
        return EntryState.objects.filter(
            state=EntryState.STATE_SAVED, entry=self, user=user
        ).exists()

    def is_deleted_by(self, user) -> bool:
        """Check if the given entry has been deleted by the given user."""
        return EntryState.objects.filter(
            state=EntryState.STATE_DELETED, entry=self, user=user
        ).exists()

    @property
    def slang_date_published(self):
        """Display a human readable, slang datetime."""
        if not self.date_published:
            return "?"
        maya_dt = maya.MayaDT.from_datetime(self.date_published)
        return maya_dt.slang_time()

    TEASER_WORDS = 15

    @property
    def teaser(self):
        """Get a displayable teaser for rows or cards."""
        text = self.summary if self.summary else self.content
        truncated_text = Truncator(text).words(self.TEASER_WORDS)
        return truncated_text

    def __str__(self):
        """Str dunder implementation."""
        return self.title

    class Meta:
        verbose_name_plural = "entries"
        unique_together = (("guid", "feed"),)


class EntryState(models.Model):
    """The user state of an entry.

    TODO unread state doesn't need to exist
    """

    # TODO consider changing SAVED/PINNED/DELETED into a proper state machine
    STATE_UNREAD = "unread"
    STATE_READ = "read"
    STATE_SAVED = "saved"
    STATE_DELETED = "deleted"
    STATE_PINNED = "pinned"
    STATE_CHOICES = [
        (STATE_UNREAD, "Unread"),
        (STATE_READ, "Read"),
        (STATE_SAVED, "Saved"),
        (STATE_DELETED, "Deleted"),
        (STATE_PINNED, "Pinned"),
    ]
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    entry = models.ForeignKey(Entry, related_name="states", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="entry_states", on_delete=models.CASCADE
    )

    @staticmethod
    def is_valid_state(state):
        """Check if the provided state is present within the available state choices."""
        return state in dict(EntryState.STATE_CHOICES)

    class Meta:
        unique_together = (("state", "user", "entry"),)


class Enclosure(models.Model):
    """A media file."""

    href = models.CharField(max_length=1000)
    file_type = models.CharField(max_length=1000)
    # TODO this seems dirty but I'm not sure of the best way to handle this
    length = models.TextField()

    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="enclosures"
    )

    def __str__(self):
        """Str representation of enclosure."""
        return self.href
