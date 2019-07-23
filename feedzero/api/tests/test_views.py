from django.urls import reverse
import pytest

from feedzero.feeds.models import EntryState


def _get_user(client):
    # TODO replace this with something less tragic
    #      I tried the typical get_user to no avail
    return client.handler._force_user


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
