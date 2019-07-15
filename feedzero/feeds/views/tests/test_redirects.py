from django.conf import settings
from django.contrib.auth import get_user
from django.urls import reverse
import pytest

from feedzero.feeds.models import EntryState


@pytest.mark.django_db
class TestEntryOffloadView:
    def _get_url(self, entry):
        return reverse(
            "feeds:entry_read",
            kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug},
        )

    def test_requires_login(self, client, entry):
        """Must require an authenticated session to access."""
        url = self._get_url(entry)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_redirects_to_entry_link(self, auth_client, entry):
        """Should redirect to entry link."""
        url = self._get_url(entry)
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == entry.link

    def test_creates_read_state(self, auth_client, entry):
        """Should create a read state entry."""
        url = self._get_url(entry)
        auth_client.get(url)
        assert EntryState.objects.filter(
            entry=entry, state=EntryState.STATE_READ, user=get_user(auth_client)
        ).exists()
