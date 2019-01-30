from django.conf import settings
from django.test import Client
from model_mommy import mommy
import pytest
from rest_framework.test import APIClient

from badfeed.feeds.models import Entry, Feed
from badfeed.users.models import ThirdPartyTokens


@pytest.fixture
def user():
    return mommy.make(settings.AUTH_USER_MODEL, username="BadUser")


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture()
def client_factory():
    def _make(user=None):
        client = Client()
        if user:
            client.force_login(user)
        return client

    return _make


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
def pocket_token(user):
    return mommy.make(ThirdPartyTokens, provider=ThirdPartyTokens.PROVIDER_POCKET)
