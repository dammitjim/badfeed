from django.conf import settings
from django.test import Client
from model_mommy import mommy
import pytest
from rest_framework.test import APIClient

from badfeed.feeds.models import EnrichedContent, Entry, EntryState, Feed
from badfeed.rules.models import FeedRule, Rule, TextMatchRule
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


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def feed_factory():
    def _make(**kwargs):
        watched_by = kwargs.pop("watched_by", None)
        feed = mommy.make(Feed, **kwargs)
        if watched_by:
            watched_by.watch(feed)
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


@pytest.fixture
def enriched_content():
    return mommy.make(EnrichedContent)


@pytest.fixture
def enriched_content_factory(**kwargs):
    def _make(**kwargs):
        return mommy.make(EnrichedContent, **kwargs)

    return _make


@pytest.fixture
def rule():
    return mommy.make(Rule)


@pytest.fixture
def rule_factory():
    def _make(**kwargs):
        return mommy.make(Rule, **kwargs)

    return _make


@pytest.fixture
def feed_rule():
    return mommy.make(FeedRule)


@pytest.fixture
def feed_rule_factory():
    def _make(**kwargs):
        return mommy.make(FeedRule, **kwargs)

    return _make


@pytest.fixture
def text_match_rule():
    return mommy.make(TextMatchRule)


@pytest.fixture
def text_match_rule_factory():
    def _make(**kwargs):
        return mommy.make(TextMatchRule, **kwargs)

    return _make
