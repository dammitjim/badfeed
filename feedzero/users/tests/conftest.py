from django.conf import settings
from model_mommy import mommy
import pytest

from feedzero.feeds.models import Entry, EntryState, Feed
from feedzero.users.models import ThirdPartyTokens


@pytest.fixture()
def registration_form_data():
    """Valid by default."""
    return {
        "username": "user1",
        "email": "user1@test.com",
        "confirm_email": "user1@test.com",
        "password1": "CoolPass!123",
        "password2": "CoolPass!123",
    }


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
def entry_state(watched_entry, user):
    return mommy.make(EntryState, entry=watched_entry, user=user)


@pytest.fixture
def third_party_token():
    return mommy.make(ThirdPartyTokens)


@pytest.fixture
def third_party_token_factory(user):
    def _make(**kwargs):
        if "user" not in kwargs:
            kwargs["user"] = user
        return mommy.make(ThirdPartyTokens, **kwargs)

    return _make
