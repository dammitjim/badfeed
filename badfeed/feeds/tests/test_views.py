from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_mommy import mommy
import pytest

from badfeed.feeds.models import Feed


@pytest.fixture
def feed():
    return mommy.make(Feed, title="My Amazing Feed!")


@pytest.mark.django_db
class TestFeedList:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()
        cls.url = reverse("feeds:feed_list")

    def test_requires_authorization(self, feed):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
