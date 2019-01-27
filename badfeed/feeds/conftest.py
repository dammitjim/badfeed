from model_mommy import mommy
import pytest

from badfeed.feeds.models import Entry, EntryState, Feed


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def feed_factory():
    def _make(**kwargs):
        feed = mommy.make(Feed, **kwargs)
        if "watched_by" in kwargs:
            kwargs["watched_by"].watch(feed)
        return feed

    return _make


@pytest.fixture()
def entry():
    return mommy.make(Entry)


@pytest.fixture()
def entry_fill():
    return mommy.make(Entry, _fill_optional=True)


@pytest.fixture()
def entry_factory(feed):
    def _make(**kwargs):
        if "feed" in kwargs:
            attached_feed = kwargs.pop("feed")
        else:
            attached_feed = feed
        return mommy.make(Entry, feed=attached_feed, **kwargs)

    return _make


@pytest.fixture()
def entry_state():
    return mommy.make(entry_state)


@pytest.fixture()
def entry_state_factory(user):
    def _make(**kwargs):
        if "user" in kwargs:
            attached_user = kwargs.pop("user")
        else:
            attached_user = user
        return mommy.make(EntryState, user=attached_user, **kwargs)

    return _make
