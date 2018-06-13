from django.urls import reverse
from rest_framework import status
import pytest

from badfeed.feeds.models import EntryState
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

    def test_patch_requires_authorization(self, anon_client):
        """When logged out, the endpoint should require authorization."""
        response = anon_client.patch(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_watches_feed(self, auth_client, user, feed):
        """A successful PATCH should watch the submitted feed."""
        response = auth_client.patch(self.url, data={"feed": feed.pk})
        assert response.status_code == status.HTTP_201_CREATED
        assert feed in user.watching.all()

    def test_patch_handles_feed_not_found(self, auth_client):
        """The PATCH endpoint should gracefully handle a feed not found error."""
        response = auth_client.patch(self.url, data={"feed": 0})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_only_watched_feeds_display(self, auth_client, watched_feed, feed):
        """The response should only contain watched feeds."""
        response = auth_client.get(self.url)
        content = response.data["results"]
        assert MyFeedSerializer(watched_feed).data in content
        assert MyFeedSerializer(feed).data not in content


@pytest.mark.django_db
class TestMyFeedDetail:
    def test_get_requires_authorization(self, anon_client, watched_feed):
        """When logged out, the endpoint should require authorization."""
        url = reverse("users:feed_detail", kwargs={"slug": watched_feed.slug})
        response = anon_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_200_when_logged_in(self, auth_client, watched_feed):
        """When logged in, the endpoint should respond 200."""
        url = reverse("users:feed_detail", kwargs={"slug": watched_feed.slug})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_requires_authorization(self, anon_client, watched_feed):
        """When logged out, the endpoint should require authorization."""
        url = reverse("users:feed_detail", kwargs={"slug": watched_feed.slug})
        response = anon_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_404_if_not_watching(self, auth_client, feed):
        """When you are not following a feed, you should not see the detail."""
        url = reverse("users:feed_detail", kwargs={"slug": feed.slug})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_response_content(self, auth_client, watched_feed):
        """Ensure the response content is serialized appropriately."""
        url = reverse("users:feed_detail", kwargs={"slug": watched_feed.slug})
        response = auth_client.get(url)
        assert response.data == MyFeedSerializer(watched_feed).data

    def test_delete_stops_watching(self, auth_client, user, watched_feed):
        """Ensure that sending DELETE unwatches the feed."""
        assert watched_feed in user.watching.all()
        url = reverse("users:feed_detail", kwargs={"slug": watched_feed.slug})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert watched_feed not in user.watching.all()

    def test_delete_invalid_feed_404s(self, auth_client):
        """Invalid slugs should return 404 on DELETE request."""
        url = reverse("users:feed_detail", kwargs={"slug": "invalid"})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMyFeedEntryDetail:
    # TODO look in pytest docs for a way to not have to duplicate the URL every time

    def test_get_requires_authorization(self, anon_client, watched_feed, watched_entry):
        """When logged out, the endpoint should require authorization."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        response = anon_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responds_200_when_logged_in(self, auth_client, watched_feed, watched_entry):
        """When logged in, the endpoint should respond 200."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_requires_authorization(self, anon_client, watched_feed, watched_entry):
        """When logged out, the endpoint should require authorization."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        response = anon_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_invalid_state_400s(self, auth_client, watched_feed, watched_entry):
        """An invalid state should raise a 400."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        response = auth_client.post(url, data={"state": "butts"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_invalid_state_400s(self, auth_client, watched_feed, watched_entry):
        """An invalid state should raise a 400."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        response = auth_client.delete(url, data={"state": "butts"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_creates_entry_state(self, auth_client, watched_feed, watched_entry, user):
        """A POST request should create a new entry state object."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        assert not EntryState.objects.filter(entry=watched_entry, user=user, state=EntryState.STATE_SAVED).exists()
        response = auth_client.post(url, data={"state": EntryState.STATE_SAVED})
        assert response.status_code == status.HTTP_201_CREATED
        assert EntryState.objects.filter(entry=watched_entry, user=user, state=EntryState.STATE_SAVED).exists()

    def test_delete_creates_entry_state(self, auth_client, watched_feed, watched_entry, user, entry_state):
        """A DELETE request should remove a entry state object."""
        url = reverse("users:feed_entry_detail", kwargs={"slug": watched_entry.slug, "feed_slug": watched_feed.slug})
        assert EntryState.objects.filter(entry=watched_entry, user=user, state=entry_state.state).exists()
        response = auth_client.delete(url, data={"state": entry_state.state})
        assert response.status_code == status.HTTP_200_OK
        assert not EntryState.objects.filter(entry=watched_entry, user=user, state=EntryState.STATE_SAVED).exists()
