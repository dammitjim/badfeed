from django.conf import settings
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed, Entry, EntryState


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
