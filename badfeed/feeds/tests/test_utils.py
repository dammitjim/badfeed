import pytest

from badfeed.feeds import utils
from badfeed.feeds.models import EntryState
from badfeed.users.models import BadFeedUser


@pytest.mark.django_db
def test_delete_entries_for_user(entry_factory, watched_feed):
    """Should create deleted entry states for each entry."""
    entries = [entry_factory(feed=watched_feed) for _ in range(10)]
    assert len(EntryState.objects.all()) == 0
    utils.delete_entries_for_user(
        entries, BadFeedUser.objects.get(watching__in=[watched_feed])
    )
    assert len(EntryState.objects.filter(state=EntryState.STATE_DELETED)) == 10


@pytest.mark.django_db
def test_pin_entries_for_user(entry_factory, watched_feed):
    """Should create pinned entry states for each entry."""
    entries = [entry_factory(feed=watched_feed) for _ in range(10)]
    assert len(EntryState.objects.all()) == 0
    utils.pin_entries_for_user(
        entries, BadFeedUser.objects.get(watching__in=[watched_feed])
    )
    assert len(EntryState.objects.filter(state=EntryState.STATE_PINNED)) == 10


@pytest.mark.django_db
def test_save_entries_for_user(entry_factory, watched_feed):
    """Should create saved entry states for each entry."""
    entries = [entry_factory(feed=watched_feed) for _ in range(10)]
    assert len(EntryState.objects.all()) == 0
    utils.save_entries_for_user(
        entries, BadFeedUser.objects.get(watching__in=[watched_feed])
    )
    assert len(EntryState.objects.filter(state=EntryState.STATE_SAVED)) == 10
