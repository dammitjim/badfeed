from django.urls import reverse
from rest_framework import status
import pytest

from badfeed.feeds.serializers import MyFeedSerializer


@pytest.mark.django_db
class TestMyFeedList:
    @classmethod
    def setup_class(cls):
        cls.url = reverse("users:feed_list")

    def test_get_requires_authorization(self, anon_client):
        """When logged out, the endpoint should require authorization."""
        response = anon_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_200_when_logged_in(self, auth_client):
        """When logged in, the endpoint should respond 200."""
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_requires_authorization(self, anon_client):
        """When logged out, the endpoint should require authorization."""
        response = anon_client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_watches_feed(self, auth_client, user, feed):
        """A successful POST should watch the submitted feed."""
        response = auth_client.post(self.url, data={"feed": feed.pk})
        assert response.status_code == status.HTTP_201_CREATED
        assert feed in user.watching.all()

    def test_post_handles_feed_not_found(self, auth_client):
        """The POST endpoint should gracefully handle a feed not found error."""
        response = auth_client.post(self.url, data={"feed": 0})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_only_watched_feeds_display(self, auth_client, watched_feed, feed):
        """The response should only contain watched feeds."""
        response = auth_client.get(self.url)
        content = response.data["results"]
        assert MyFeedSerializer(watched_feed).data in content
        assert MyFeedSerializer(feed).data not in content
