from django.conf import settings
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestFeedSearch:
    def setup(self):
        self.url = reverse("feeds:search")

    def _search_url(self, term):
        return f"{self.url}?term={term}"

    def test_results_case_insensitive(self, auth_client, feed_factory):
        """The search should be case insensitive."""
        feed1 = feed_factory(title="BUTTS")
        feed2 = feed_factory(title="Butts")
        feed3 = feed_factory(title="Booty")
        response = auth_client.get(self._search_url("butts"))
        assert feed1 in response.context["object_list"]
        assert feed2 in response.context["object_list"]
        assert feed3 not in response.context["object_list"]

    def test_results_exact_match(self, auth_client, feed):
        """The search should match the title."""
        response = auth_client.get(self._search_url(feed.title))
        assert feed in response.context["object_list"]

    def test_search_term_in_context(self, auth_client):
        """Should load the search term into the context."""
        response = auth_client.get(self._search_url("test"))
        assert "search_term" in response.context

    def test_renders(self, auth_client):
        """The search page should render."""
        response = auth_client.get(self._search_url("test"))
        assert response.status_code == 200

    def test_requires_term_get_param(self, auth_client):
        """The search page should require the term GET argument."""
        response = auth_client.get(self.url)
        assert response.status_code == 404

    def test_requires_login(self, client):
        """The view should require a user to be logged in."""
        response = client.get(self._search_url("test"))
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next=/f/search/%3Fterm%3Dtest"
