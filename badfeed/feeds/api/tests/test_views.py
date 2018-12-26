from django.urls import reverse
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestFeedList:
    @classmethod
    def setup_class(cls):
        cls.url = reverse("api_v1:feeds:feed_list")

    def test_requires_authorization(self, anon_api_client):
        """When logged out, the endpoint should respond unauthorized."""
        response = anon_api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_200_when_logged_in(self, auth_api_client):
        """When logged in, the endpoint should respond 200."""
        response = auth_api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
