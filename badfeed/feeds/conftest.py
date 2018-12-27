from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def feed_factory():
    def _make(**kwargs):
        return mommy.make(Feed, **kwargs)

    return _make


@pytest.fixture()
def entry():
    return mommy.make(Entry)


@pytest.fixture()
def entry_factory(feed):
    def _make(**kwargs):
        return mommy.make(Entry, feed=feed, **kwargs)

    return _make
