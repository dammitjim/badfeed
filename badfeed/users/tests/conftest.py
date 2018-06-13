from django.conf import settings
from rest_framework.test import APIClient
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def entry(feed):
    return mommy.make(Entry, feed=feed, title="My Amazing Entry!")


@pytest.fixture
def user():
    return mommy.make(settings.AUTH_USER_MODEL, username="BadUser")


@pytest.fixture
def watched_feed(user):
    feed = mommy.make(Feed, title="My Watched Feed!")
    user.watching.add(feed)
    user.save()
    return feed


@pytest.fixture
def watched_entry(watched_feed):
    return mommy.make(Entry, feed=watched_feed, title="My Amazing Entry!")


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client
