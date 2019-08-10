from django.urls import reverse
import pytest

from feedzero.feeds.models import EntryState


@pytest.mark.django_db
class TestEntryListView:
    def setup(self):
        self.url = reverse("api:entry_list")

    def test_requires_login(self, api_client):
        """Should require an authenticated user to access."""
        response = api_client.get(self.url)
        assert response.status_code == 403

    def test_responds_200(self, auth_api_client, entry_factory, watched_feed):
        """Should respond 200 without error."""
        (feed, user) = watched_feed
        [entry_factory(feed=feed) for _ in range(5)]
        response = auth_api_client.get(self.url)
        assert response.status_code == 200

    def test_lists_only_unread_entries(
        self, auth_api_client, entry_factory, watched_feed
    ):
        """Should only list unread entries for the user."""
        (feed, user) = watched_feed
        entries = [entry_factory(feed=feed) for _ in range(5)]
        for entry in entries[:3]:
            entry.mark_deleted(auth_api_client.user)
        response = auth_api_client.get(self.url)
        assert response.json()["count"] == 2

    def test_omits_state(self, auth_api_client, entry_factory, watched_feed):
        """Should not include any state information in this payload."""
        (feed, user) = watched_feed
        entry_factory(feed=feed)
        data = auth_api_client.get(self.url).json()
        for entry in data["results"]:
            assert "state" not in entry


@pytest.mark.django_db
class TestPinnedEntryListView:
    def setup(self):
        self.url = reverse("api:pinned_entry_list")

    def test_requires_login(self, api_client):
        """Should require an authenticated user to access."""
        response = api_client.get(self.url)
        assert response.status_code == 403

    def test_responds_200(self, auth_api_client, entry_factory, watched_feed):
        """Should respond 200 without error."""
        (feed, user) = watched_feed
        entries = [entry_factory(feed=feed) for _ in range(5)]
        [entry.mark_pinned(user) for entry in entries]
        response = auth_api_client.get(self.url)
        assert response.status_code == 200

    def test_lists_only_pinned_entries(
        self, auth_api_client, entry_factory, watched_feed
    ):
        """Should only list pinned entries for the user."""
        (feed, user) = watched_feed
        entries = [entry_factory(feed=feed) for _ in range(5)]
        [entry.mark_pinned(user) for entry in entries[:3]]
        response = auth_api_client.get(self.url)
        assert response.json()["count"] == 3


@pytest.mark.django_db
class TestFeedListView:
    def setup(self):
        self.url = reverse("api:feed_list")

    def test_requires_login(self, api_client):
        """Should require an authenticated user to access."""
        response = api_client.get(self.url)
        assert response.status_code == 403

    def test_responds_200(self, auth_api_client, feed_factory):
        """Should respond 200 from a basic request."""
        pass

    def test_filter_only_watched_feeds(self, auth_api_client, feed_factory):
        """Should only return watched feeds if passed only=user as a GET param."""
        pass


@pytest.mark.django_db
class TestEntryStateCreationView:
    def setup(self):
        self.url = reverse("api:state_create")

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
            self.url, {"actions": [{"state": "pinned"}]}, format="json"
        )
        assert response.status_code == 400

    def test_no_matching_entry_does_nothing(self, auth_api_client):
        """If there is no matching ID, do nothing."""
        initial_length = len(EntryState.objects.all())
        response = auth_api_client.post(
            self.url,
            {"actions": [{"state": "pinned", "entry_id": "-1"}]},
            format="json",
        )
        assert response.status_code == 404
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
        response = auth_api_client.post(
            self.url,
            {"actions": [{"state": state, "entry_id": entry.id}]},
            format="json",
        )
        assert response.status_code == 200
        assert EntryState.objects.filter(
            entry=entry, state=state, user=auth_api_client.user
        ).exists()

    def test_bulk_mark_different_entries(self, auth_api_client, entry_factory):
        """Should be able to mark different entries with different states."""
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
                entry__id=action["entry_id"],
                state=action["state"],
                user=auth_api_client.user,
            ).exists()
