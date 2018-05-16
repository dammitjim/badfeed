from django.db.utils import IntegrityError
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry


@pytest.fixture
def feed():
    return mommy.make(
        Feed,
        name='My Amazing Feed!'
    )

@pytest.fixture
def entry():
    return mommy.make(
        Entry,
        name='My Amazing Entry!'
    )

@pytest.mark.django_db
class TestFeedModel:

    def test_dunder_str(self, feed):
        """The model should render the name as the string."""
        assert str(feed) == feed.name

    def test_generated_slug(self, feed):
        """The model should generate an appropriate slug."""
        assert feed.slug == 'my-amazing-feed'


@pytest.mark.django_db
class TestEntryModel:

    def test_dunder_str(self, entry):
        """The model should render the name as the string."""
        assert str(entry) == entry.name

    def test_clean_checks_duplicates(self, entry):
        """A duplicated entry within a feed should raise an IntegrityError."""
        with pytest.raises(IntegrityError):
            entry_dup = mommy.make(
                Entry,
                remote_id=entry.remote_id,
                feed=entry.feed,
            )

    def test_slug_handles_duplicates_per_feed(self, entry):
        """A duplicated slug should not raise, should handle."""
        entry_dup = mommy.make(
            Entry,
            feed=entry.feed,
            name=entry.name,
        )
        assert entry_dup.slug == 'my-amazing-entry-1'
