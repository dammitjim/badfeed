from django.conf import settings
from django.test import Client
from rest_framework.test import APIClient
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


@pytest.fixture
def anon_api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client
