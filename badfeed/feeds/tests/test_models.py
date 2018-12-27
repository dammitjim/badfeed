from django.db.utils import IntegrityError
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry, EntryState


@pytest.mark.django_db
class TestFeedModel:
    def test_dunder_str(self, feed):
        """The model should render the name as the string."""
        assert str(feed) == feed.title

    def test_generated_slug(self, feed):
        """The model should generate an appropriate slug."""
        assert feed.slug == "my-amazing-feed"

    def test_handles_duplicated_slug(self):
        """The model should generate an appropriate slug if a duplicate is found."""
        mommy.make(Feed, title="This is only a test")
        feed_dup = mommy.make(Feed, title="This is only a test")
        assert feed_dup.slug == "this-is-only-a-test-1"


@pytest.mark.django_db
class TestEntryStateModel:
    def test_unique_together_constraint(self, entry, user):
        """The model should forbid state, user, entry combo duplicates."""
        mommy.make(EntryState, entry=entry, state=EntryState.STATE_PINNED, user=user)
        with pytest.raises(IntegrityError):
            mommy.make(EntryState, entry=entry, state=EntryState.STATE_PINNED, user=user)

    def test_pinned_and_read(self, entry, user):
        """The model should allow an entry to be both pinned and read."""
        mommy.make(EntryState, entry=entry, state=EntryState.STATE_PINNED, user=user)
        mommy.make(EntryState, entry=entry, state=EntryState.STATE_READ, user=user)

    def test_saved_and_pinned(self, entry, user):
        """The model should allow an entry to be both pinned and saved."""
        mommy.make(EntryState, entry=entry, state=EntryState.STATE_PINNED, user=user)
        mommy.make(EntryState, entry=entry, state=EntryState.STATE_SAVED, user=user)


@pytest.mark.django_db
class TestEntryModel:
    def test_dunder_str(self, entry):
        """The model should render the name as the string."""
        assert str(entry) == entry.title

    def test_clean_checks_duplicates(self, entry):
        """A duplicated entry within a feed should raise an IntegrityError."""
        with pytest.raises(IntegrityError):
            mommy.make(Entry, guid=entry.guid, feed=entry.feed)

    def test_slug_handles_duplicates_per_feed(self):
        """A duplicated slug should not raise, should handle."""
        entry = mommy.make(Entry, title="My Amazing Entry!")
        entry_dup = mommy.make(Entry, feed=entry.feed, title=entry.title)
        assert entry_dup.slug == "my-amazing-entry-1"

    def test_feed_guid_unique_together_constraint(self, entry):
        """A duplicated guid for the same feed should raise IntegrityError."""
        with pytest.raises(IntegrityError):
            mommy.make(Entry, feed=entry.feed, guid=entry.guid)

    def test_feed_guid_unique_together_allowed(self, entry):
        """Guid uniqueness should only be bound to the same feed."""
        mommy.make(Entry, guid=entry.guid)

    def test_feed_deletion_cascades_deletion(self, entry):
        """Entry should be deleted when an associated Feed is deleted."""
        entry.feed.delete()
        with pytest.raises(Entry.DoesNotExist):
            entry.refresh_from_db()

    def test_author_deletion_sets_null(self, entry_fill):
        """Entry should be preserved when an associated Author is deleted."""
        entry_fill.author.delete()
        entry_fill.refresh_from_db()
        assert entry_fill.author is None

    def test_mark_read_by_creates(self, entry, user):
        """Should create a read by state."""
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_READ).exists()
        entry.mark_read_by(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_READ)) == 1

    def test_mark_read_by_get(self, entry, user):
        """Should reuse existing state if exists."""
        entry.mark_read_by(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_READ)) == 1
        entry.mark_read_by(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_READ)) == 1

    def test_mark_pinned_creates(self, entry, user):
        """Should create a pinned state."""
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED).exists()
        entry.mark_pinned(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED)) == 1

    def test_mark_pinned_get(self, entry, user):
        """Should reuse existing state if exists."""
        entry.mark_pinned(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED)) == 1
        entry.mark_pinned(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED)) == 1

    def test_mark_unpinned_deletes(self, entry, user):
        """Should delete pinned state."""
        entry.mark_pinned(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED)) == 1
        entry.mark_unpinned(user)
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED).exists()

    def test_mark_unpinned_allows_state_not_exists(self, entry, user):
        """If the state does not exist, should fail silently."""
        entry.mark_unpinned(user)
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_PINNED).exists()

    def test_mark_saved_creates(self, entry, user):
        """Should create a saved state."""
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED).exists()
        entry.mark_saved(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED)) == 1

    def test_mark_saved_get(self, entry, user):
        """Should reuse existing state if exists."""
        entry.mark_saved(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED)) == 1
        entry.mark_saved(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED)) == 1

    def test_mark_unsaved_deletes(self, entry, user):
        """Should delete saved state."""
        entry.mark_saved(user)
        assert len(EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED)) == 1
        entry.mark_unsaved(user)
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED).exists()

    def test_mark_unsaved_allows_state_not_exists(self, entry, user):
        """If the state does not exist, should fail silently."""
        entry.mark_unsaved(user)
        assert not EntryState.objects.filter(entry=entry, user=user, state=EntryState.STATE_SAVED).exists()
