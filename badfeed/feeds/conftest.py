from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def feed_factory():
    def _make(**kwargs):
        return mommy.make(Feed, **kwargs)

    return _make
