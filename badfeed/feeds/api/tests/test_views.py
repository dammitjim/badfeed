# from django.contrib.auth import get_user
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestGenericFeedDashboardView:
    def setup(self):
        """Set up common variables."""
        self.url = reverse("api_feeds:dash")

    def test_only_watched_feeds(self):
        """Should only return feeds which are watched by the user."""
        pass

    def test_orders_entries_by_entry_publishing(self):
        """Entries should be ordered by publish date."""
        pass

    def test_orders_feeds_by_entry_publishing(self):
        """Feeds should be ordered by publish date of entries."""
        pass

    def test_data_paginated(self, auth_api_client):
        """Should respond with a paginated format."""
        response = auth_api_client.get(self.url)
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

    def test_data_respects_pagination(self):
        """Should be paginateable."""
        pass

    def test_only_unread_entries(self):
        """Only unread entries should be present in a feed."""
        pass

    def test_only_feeds_with_unread_entries(self):
        """Feeds with only read entries should be hidden."""
        pass

    def test_no_unread_empty_list(self, auth_api_client, feed_factory):
        """If no unread entries in watched feeds, should return empty list."""
        # user = get_user(auth_api_client)
        # feed1 = feed_factory(watched_by=user)
        # feed2 = feed_factory(watched_by=user)
        response = auth_api_client.get(self.url)
        assert response.data["results"] == []

    def test_partial_unread_only_returns_feeds_with_unread(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """If only X have unread entries out of watched, only return X."""
        pass

    def test_responds(self, auth_api_client):
        """Should respond at the most basic level to a logged in user."""
        response = auth_api_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, api_client):
        """The api should only respond to logged in users."""
        response = api_client.get(self.url)
        assert response.status_code == 403
