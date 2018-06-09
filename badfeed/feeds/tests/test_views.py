from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.fixture
def user():
    return mommy.make(settings.AUTH_USER_MODEL)


@pytest.mark.django_db
class TestFeedList:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()
        cls.url = reverse("feeds:feed_list")

    def test_requires_authorization(self):
        """When logged out, the endpoint should respond unauthorized."""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_200_when_logged_in(self, user):
        """When logged in, the endpoint should respond 200."""
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
