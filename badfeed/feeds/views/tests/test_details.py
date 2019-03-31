from django.conf import settings
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestFeedDetail:
    def _get_url(self, feed):
        return reverse("feeds:detail", kwargs={"slug": feed.slug})

    def test_requires_login(self, client, feed):
        """Must require an authenticated session to access."""
        url = self._get_url(feed)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_renders(self, auth_client, feed):
        """Renders successfully."""
        url = self._get_url(feed)
        response = auth_client.get(url)
        assert response.status_code == 200
