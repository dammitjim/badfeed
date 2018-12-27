from django.conf import settings
from django.test import Client
from model_mommy import mommy
import pytest


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
