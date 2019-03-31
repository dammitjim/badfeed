from django.conf import settings
from django.urls import reverse
import pytest

from badfeed.feeds.models import EntryState


@pytest.mark.django_db
class TestPinnedEntriesListView:
    def setup(self):
        self.url = reverse("feeds:pinned_entries")

    def test_renders(self, auth_client):
        """The view should render."""
        response = auth_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, client):
        """The view requires the user be logged in."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    def test_only_returns_pinned_entries(self, auth_client, entry_state_factory, user):
        """The view should only return entries for pinned feeds."""
        pinned_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_PINNED).entry
            for _ in range(5)
        ]
        other_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry
            for _ in range(5)
        ]
        response = auth_client.get(self.url)
        for entry in pinned_entries:
            assert entry in response.context["page_obj"].object_list
        for entry in other_entries:
            assert entry not in response.context["page_obj"].object_list


@pytest.mark.django_db
class TestSavedEntriesListView:
    def setup(self):
        self.url = reverse("feeds:saved_entries")

    def test_renders(self, auth_client):
        """The view should render."""
        response = auth_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, client):
        """The view requires the user be logged in."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    def test_only_returns_saved_entries(self, auth_client, entry_state_factory, user):
        """The view should only return entries for saved feeds."""
        saved_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry
            for _ in range(5)
        ]
        other_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_DELETED).entry
            for _ in range(5)
        ]
        response = auth_client.get(self.url)
        for entry in saved_entries:
            assert entry in response.context["page_obj"].object_list
        for entry in other_entries:
            assert entry not in response.context["page_obj"].object_list


@pytest.mark.django_db
class TestArchivedEntriesListView:
    def setup(self):
        self.url = reverse("feeds:archived_entries")

    def test_renders(self, auth_client):
        """The view should render."""
        response = auth_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, client):
        """The view requires the user be logged in."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    def test_only_returns_archived_entries(
        self, auth_client, entry_state_factory, user
    ):
        """The view should only return entries for archived feeds."""
        archived_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_DELETED).entry
            for _ in range(5)
        ]
        other_entries = [
            entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry
            for _ in range(5)
        ]
        response = auth_client.get(self.url)
        for entry in archived_entries:
            assert entry in response.context["page_obj"].object_list
        for entry in other_entries:
            assert entry not in response.context["page_obj"].object_list
