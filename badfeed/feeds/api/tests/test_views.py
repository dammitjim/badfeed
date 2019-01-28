from django.urls import reverse
import maya
import pytest

from badfeed.feeds.models import EntryState


@pytest.mark.django_db
class TestGenericFeedDashboardView:
    def setup(self):
        """Set up common variables."""
        self.url = reverse("api_feeds:dash")

    def _get_user(self, client):
        # TODO replace this with something less tragic
        #      I tried the typical get_user to no avail
        return client.handler._force_user

    def test_only_watched_feeds(self, auth_api_client, feed_factory, entry_factory):
        """Should only return feeds which are watched by the user."""
        user = self._get_user(auth_api_client)
        # partially actioned entries
        feed = feed_factory(watched_by=user)
        entry_factory(feed=feed)
        feed2 = feed_factory()
        entry_factory(feed=feed2)

        response = auth_api_client.get(self.url)
        assert response.data["count"] == 1

    def test_orders_entries_by_entry_publishing(
        self, auth_api_client, feed_factory, entry_factory
    ):
        """Entries should be ordered by publish date."""
        user = self._get_user(auth_api_client)
        # partially actioned entries
        feed = feed_factory(watched_by=user)
        oldest_entry = entry_factory(
            feed=feed, date_published=maya.now().subtract(days=3).datetime()
        )
        mid_entry = entry_factory(
            feed=feed, date_published=maya.now().subtract(days=2).datetime()
        )
        newest_entry = entry_factory(
            feed=feed, date_published=maya.now().subtract(days=1).datetime()
        )

        response = auth_api_client.get(self.url)
        entries = response.data["results"][0]["entries"]
        assert [entry["id"] for entry in entries] == [
            newest_entry.id,
            mid_entry.id,
            oldest_entry.id,
        ]

    def test_orders_feeds_by_entry_publishing(
        self, auth_api_client, feed_factory, entry_factory
    ):
        """Feeds should be ordered by publish date of entries."""
        user = self._get_user(auth_api_client)
        feed1 = feed_factory(watched_by=user)
        feed2 = feed_factory(watched_by=user)
        feed3 = feed_factory(watched_by=user)

        entry_factory(feed=feed1, date_published=maya.now().subtract(days=3).datetime())
        entry_factory(feed=feed2, date_published=maya.now().subtract(days=2).datetime())
        entry_factory(feed=feed3, date_published=maya.now().subtract(days=1).datetime())

        response = auth_api_client.get(self.url)
        feeds = [feed["feed"]["id"] for feed in response.data["results"]]
        assert feeds == [feed3.id, feed2.id, feed1.id]

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

    def test_actioned_feeds_ignored(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """Actioned feeds should not show.

        An actioned feed is one whereby all entries contained within have been
        actioned. AKA a state exists for each for this user.
        """
        user = self._get_user(auth_api_client)
        feed = feed_factory(watched_by=user)

        # create two actioned entries
        entry1 = entry_factory(feed=feed)
        entry_state_factory(user=user, entry=entry1, state=EntryState.STATE_PINNED)
        entry2 = entry_factory(feed=feed)
        entry_state_factory(user=user, entry=entry2, state=EntryState.STATE_DELETED)

        response = auth_api_client.get(self.url)
        assert response.data["count"] == 0

    def test_feeds_without_entries_ignored(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """If a feed has no entries at all, it should not appear on the dash.

        Unlikely to happen, but nice to account for.
        """
        user = self._get_user(auth_api_client)
        feed_factory(watched_by=user)
        response = auth_api_client.get(self.url)
        assert response.data["count"] == 0

    def test_feeds_with_partially_actioned_entries_included(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """If a feed has some actioned, some unactioned entries, it should be included."""
        user = self._get_user(auth_api_client)
        # partially actioned entries
        feed = feed_factory(watched_by=user)
        entry_factory(feed=feed)
        entry = entry_factory(feed=feed)
        entry_state_factory(user=user, entry=entry, state=EntryState.STATE_DELETED)

        response = auth_api_client.get(self.url)
        assert response.data["count"] == 1

    def test_feed_entries_big_badger(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """Culmination of all the individual unit tests.

        I know this breaks tradition and is a shite unit test, but this area of the code
        needs to work absolutely.

        TODO remove this when you're confident it's all gravy for the above smaller tests.
        """
        user = self._get_user(auth_api_client)

        # first create an unread entry in a watched feed
        feed1 = feed_factory(watched_by=user)
        entry_factory(feed=feed1)

        # then create a watched feed with only actioned entries
        feed2 = feed_factory(watched_by=user)
        entry2 = entry_factory(feed=feed2)
        entry_state_factory(user=user, entry=entry2, state=EntryState.STATE_PINNED)
        entry3 = entry_factory(feed=feed2)
        entry_state_factory(user=user, entry=entry3, state=EntryState.STATE_DELETED)

        # partially actioned entries
        feed3 = feed_factory(watched_by=user)
        entry_factory(feed=feed3)
        entry5 = entry_factory(feed=feed3)
        entry_state_factory(user=user, entry=entry5, state=EntryState.STATE_DELETED)

        # control feed to make sure blank badgers don't slip through
        feed_factory(watched_by=user)

        response = auth_api_client.get(self.url)
        assert response.data["count"] == 2

    def test_no_unread_empty_list(self, auth_api_client, feed_factory):
        """If no unread entries in watched feeds, should return empty list."""
        user = self._get_user(auth_api_client)
        feed_factory(watched_by=user)
        feed_factory(watched_by=user)
        response = auth_api_client.get(self.url)
        assert response.data["results"] == []

    def test_responds(self, auth_api_client):
        """Should respond at the most basic level to a logged in user."""
        response = auth_api_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, api_client):
        """The api should only respond to logged in users."""
        response = api_client.get(self.url)
        assert response.status_code == 403
