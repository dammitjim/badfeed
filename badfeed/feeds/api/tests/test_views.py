from django.urls import reverse
import maya
import pytest

from badfeed.feeds.models import EntryState


def _get_user(client):
    # TODO replace this with something less tragic
    #      I tried the typical get_user to no avail
    return client.handler._force_user


@pytest.mark.django_db
class TestGenericFeedDashboardView:
    def setup(self):
        """Set up common variables."""
        self.url = reverse("api_feeds:dash")

    def test_only_watched_feeds(self, auth_api_client, feed_factory, entry_factory):
        """Should only return feeds which are watched by the user."""
        user = _get_user(auth_api_client)
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
        user = _get_user(auth_api_client)
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
        user = _get_user(auth_api_client)
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
        # TODO implement this when you come around to figuring out how this will work.
        pass

    def test_only_unread_entries(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """Only unread entries should be present in a feed."""
        user = _get_user(auth_api_client)
        feed = feed_factory(watched_by=user)
        entry1 = entry_factory(feed=feed)
        entry_state_factory(user=user, entry=entry1, state=EntryState.STATE_PINNED)
        entry2 = entry_factory(
            feed=feed, date_published=maya.now().subtract(days=1).datetime()
        )
        entry3 = entry_factory(
            feed=feed, date_published=maya.now().subtract(days=2).datetime()
        )

        response = auth_api_client.get(self.url)
        entry_ids = [entry["id"] for entry in response.data["results"][0]["entries"]]
        assert entry_ids == [entry2.id, entry3.id]
        assert len(entry_ids) == 2

    def test_actioned_feeds_ignored(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """Actioned feeds should not show.

        An actioned feed is one whereby all entries contained within have been
        actioned. AKA a state exists for each for this user.
        """
        user = _get_user(auth_api_client)
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
        user = _get_user(auth_api_client)
        feed_factory(watched_by=user)
        response = auth_api_client.get(self.url)
        assert response.data["count"] == 0

    def test_feeds_with_partially_actioned_entries_included(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """If a feed has some actioned, some unactioned entries, it should be included."""
        user = _get_user(auth_api_client)
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
        user = _get_user(auth_api_client)

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
        user = _get_user(auth_api_client)
        feed_factory(watched_by=user)
        feed_factory(watched_by=user)
        response = auth_api_client.get(self.url)
        assert response.data["results"] == []

    def test_orders_feeds_by_entry_date_published(
        self, auth_api_client, feed_factory, entry_factory, entry_state_factory
    ):
        """Feeds should be ordered by the date published of their subsequent entries."""
        user = _get_user(auth_api_client)
        feed1 = feed_factory(watched_by=user)
        entry_factory(feed=feed1, date_published=maya.now().subtract(days=3).datetime())

        feed2 = feed_factory(watched_by=user)
        entry_factory(feed=feed2, date_published=maya.now().subtract(days=1).datetime())

        feed3 = feed_factory(watched_by=user)
        entry_factory(feed=feed3, date_published=maya.now().subtract(days=2).datetime())

        response = auth_api_client.get(self.url)
        assert response.data["count"] == 3

        results = response.data["results"]
        assert results[0]["feed"]["id"] == feed2.pk
        assert results[1]["feed"]["id"] == feed3.pk
        assert results[2]["feed"]["id"] == feed1.pk

    def test_responds(self, auth_api_client):
        """Should respond at the most basic level to a logged in user."""
        response = auth_api_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, api_client):
        """The api should only respond to logged in users."""
        response = api_client.get(self.url)
        assert response.status_code == 403


@pytest.mark.django_db
class TestEntryStateCreationView:
    def setup(self):
        self.url = reverse("api_feeds:state")

    def test_requires_login(self, api_client):
        """You must be logged in to create an entry state."""
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == 403

    def test_blank_body_raises_400(self, auth_api_client):
        """A blank POST body should raise a 400 error."""
        response = auth_api_client.post(self.url, {}, format="json")
        assert response.status_code == 400

    def test_state_required(self, auth_api_client):
        """The state attribute is required."""
        response = auth_api_client.post(
            self.url, {"actions": [{"entry_id": "1"}]}, format="json"
        )
        assert response.status_code == 400

    def test_entry_id_required(self, auth_api_client):
        """The entry_id attribute is required."""
        response = auth_api_client.post(
            self.url, {"actions": [{"state": "1"}]}, format="json"
        )
        assert response.status_code == 400

    def test_no_matching_entry_does_nothing(self, auth_api_client):
        """If there is no matching ID, do nothing."""
        initial_length = len(EntryState.objects.all())
        response = auth_api_client.post(
            self.url, {"actions": [{"state": "1", "entry_id": "-1"}]}, format="json"
        )
        assert response.status_code == 200
        assert len(EntryState.objects.all()) == initial_length

    @pytest.mark.parametrize(
        "state",
        [
            EntryState.STATE_READ,
            EntryState.STATE_SAVED,
            EntryState.STATE_PINNED,
            EntryState.STATE_DELETED,
        ],
    )
    def test_mark_entry_state(self, state, auth_api_client, entry):
        """When submitted as an action, the entry should be marked as read by."""
        user = _get_user(auth_api_client)
        response = auth_api_client.post(
            self.url,
            {"actions": [{"state": state, "entry_id": entry.id}]},
            format="json",
        )
        assert response.status_code == 200
        assert EntryState.objects.filter(entry=entry, state=state, user=user).exists()

    def test_bulk_mark_different_entries(self, auth_api_client, entry_factory):
        """Should be able to mark different entries with different states."""
        user = _get_user(auth_api_client)
        entries = [entry_factory() for _ in range(4)]
        states = [
            EntryState.STATE_READ,
            EntryState.STATE_SAVED,
            EntryState.STATE_PINNED,
            EntryState.STATE_DELETED,
        ]

        actions = [
            {"state": state, "entry_id": entries[i].id}
            for i, state in enumerate(states)
        ]

        response = auth_api_client.post(self.url, {"actions": actions}, format="json")
        assert response.status_code == 200

        for action in actions:
            assert EntryState.objects.filter(
                entry__id=action["entry_id"], state=action["state"], user=user
            ).exists()
