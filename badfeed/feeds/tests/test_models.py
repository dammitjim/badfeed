from django.db.utils import IntegrityError
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def entry():
    return mommy.make(Entry, title="My Amazing Entry!", _fill_optional=True)


@pytest.mark.django_db
class TestFeedModel:
    def test_dunder_str(self, feed):
        """The model should render the name as the string."""
        assert str(feed) == feed.title

    def test_generated_slug(self, feed):
        """The model should generate an appropriate slug."""
        assert feed.slug == "my-amazing-feed"


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

    def test_author_deletion_sets_null(self, entry):
        """Entry should be preserved when an associated Author is deleted."""
        entry.author.delete()
        entry.refresh_from_db()
        assert entry.author is None
