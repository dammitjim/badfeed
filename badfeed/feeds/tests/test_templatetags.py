from django.test import RequestFactory
from django.template import Template, Context
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestPinButton:
    def setup(self):
        self.template = Template("{% load feed_tags %}{% pin_button entry %}")

    @pytest.fixture()
    def authenticated_request(self, user):
        request = RequestFactory().get("/")
        request.user = user
        return request

    def test_is_pinned(self, entry_factory, authenticated_request):
        """If pinned, should have an option to unpin."""
        entry = entry_factory()
        entry.mark_pinned(authenticated_request.user)

        output = self.template.render(Context({"request": authenticated_request, "entry": entry}))

        expected_url = reverse("feeds:entry_unpin", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})
        assert expected_url in output

    def test_is_not_pinned(self, entry, authenticated_request):
        """If not pinned, should have an option to pin."""
        output = self.template.render(Context({"request": authenticated_request, "entry": entry}))

        expected_url = reverse("feeds:entry_pin", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})
        assert expected_url in output


@pytest.mark.django_db
class TestSaveButton:
    def setup(self):
        self.template = Template("{% load feed_tags %}{% save_button entry %}")

    @pytest.fixture()
    def authenticated_request(self, user):
        request = RequestFactory().get("/")
        request.user = user
        return request

    def test_is_saved(self, entry_factory, authenticated_request):
        """If saved, should have an option to unpin."""
        entry = entry_factory()
        entry.mark_saved(authenticated_request.user)

        output = self.template.render(Context({"request": authenticated_request, "entry": entry}))

        expected_url = reverse("feeds:entry_unsave", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})
        assert expected_url in output

    def test_is_not_saved(self, entry, authenticated_request):
        """If not saved, should have an option to pin."""
        output = self.template.render(Context({"request": authenticated_request, "entry": entry}))

        expected_url = reverse("feeds:entry_save", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})
        assert expected_url in output
