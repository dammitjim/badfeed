from django.conf import settings
from django.test import Client
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry


@pytest.fixture
def user():
    return mommy.make(settings.AUTH_USER_MODEL, username="BadUser")


@pytest.fixture
def client():
    return Client()


@pytest.fixture()
def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def watched_feed(user):
    feed = mommy.make(Feed, title="My Watched Feed!")
    user.watching.add(feed)
    user.save()
    return feed


@pytest.fixture
def watched_entry(watched_feed):
    return mommy.make(Entry, feed=watched_feed, title="My Amazing Entry!")
