from django.contrib.auth import get_user
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
import pytest

from badfeed.feeds.models import EntryState
from badfeed.feeds.views import EntryPinToggleView, EntrySaveToggleView, FeedWatchToggleView


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
        assert response.url == f"{settings.LOGIN_URL}?next=/search/%3Fterm%3Dtest"


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


@pytest.mark.django_db
class TestEntryOffloadView:
    def _get_url(self, entry):
        return reverse("feeds:entry_read", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

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
        assert EntryState.objects.filter(entry=entry, state=EntryState.STATE_READ, user=get_user(auth_client)).exists()


@pytest.mark.django_db
class TestEntryPinToggleView:
    def _get_pin_url(self, entry):
        return reverse("feeds:entry_pin", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def _get_unpin_url(self, entry):
        return reverse("feeds:entry_unpin", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def test_required_kwargs(self):
        """The view requires the `should_pin` kwarg."""
        with pytest.raises(ImproperlyConfigured):
            EntryPinToggleView()

    def test_requires_login(self, client, entry):
        """Must require an authenticated session to access."""
        url = self._get_pin_url(entry)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_object_not_found_404s(self, auth_client, entry):
        """If an object cannot be matched via slugs, return 404."""
        url = self._get_pin_url(entry)
        entry.delete()
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_should_pin_creates_state(self, auth_client, entry):
        """If should_pin is true, create the corresponding state object."""
        assert not EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_PINNED, entry=entry
        ).exists()
        url = self._get_pin_url(entry)
        auth_client.get(url)
        assert EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_PINNED, entry=entry
        ).exists()

    def test_unpin_deletes_state(self, auth_client, entry):
        """If should_pin is false, the corresponding state is deleted."""
        user = get_user(auth_client)
        entry.mark_pinned(user)
        assert EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_PINNED, entry=entry
        ).exists()
        url = self._get_unpin_url(entry)
        auth_client.get(url)
        assert not EntryState.objects.filter(user=user, state=EntryState.STATE_PINNED, entry=entry).exists()

    def test_redirect_to_feed(self, auth_client, entry):
        """If all goes well, redirect to the feed."""
        url = self._get_pin_url(entry)
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("feeds:my_entries")


@pytest.mark.django_db
class TestEntryDeleteToggleView:
    def _get_delete_url(self, entry):
        return reverse("feeds:entry_delete", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def _get_undelete_url(self, entry):
        return reverse("feeds:entry_undelete", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def test_required_kwargs(self):
        """The view requires the `should_delete` kwarg."""
        with pytest.raises(ImproperlyConfigured):
            EntrySaveToggleView()

    def test_requires_login(self, client, entry):
        """Must require an authenticated session to access."""
        url = self._get_delete_url(entry)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_object_not_found_404s(self, auth_client, entry):
        """If an object cannot be matched via slugs, return 404."""
        url = self._get_delete_url(entry)
        entry.delete()
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_should_delete_creates_state(self, auth_client, entry):
        """If should_delete is true, create the corresponding state object."""
        assert not EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_DELETED, entry=entry
        ).exists()
        url = self._get_delete_url(entry)
        auth_client.get(url)
        assert EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_DELETED, entry=entry
        ).exists()

    def test_undelete_deletes_state(self, auth_client, entry):
        """If should_delete is false, the corresponding state is deleted."""
        user = get_user(auth_client)
        entry.mark_deleted(user)
        assert EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_DELETED, entry=entry
        ).exists()
        url = self._get_undelete_url(entry)
        auth_client.get(url)
        assert not EntryState.objects.filter(user=user, state=EntryState.STATE_DELETED, entry=entry).exists()

    def test_redirect_to_feed(self, auth_client, entry):
        """If all goes well, redirect to the feed."""
        url = self._get_delete_url(entry)
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("feeds:my_entries")


@pytest.mark.django_db
class TestEntrySaveToggleView:
    def _get_save_url(self, entry):
        return reverse("feeds:entry_save", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def _get_unsave_url(self, entry):
        return reverse("feeds:entry_unsave", kwargs={"feed_slug": entry.feed.slug, "entry_slug": entry.slug})

    def test_required_kwargs(self):
        """The view requires the `should_save` kwarg."""
        with pytest.raises(ImproperlyConfigured):
            EntrySaveToggleView()

    def test_requires_login(self, client, entry):
        """Must require an authenticated session to access."""
        url = self._get_save_url(entry)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_object_not_found_404s(self, auth_client, entry):
        """If an object cannot be matched via slugs, return 404."""
        url = self._get_save_url(entry)
        entry.delete()
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_should_save_creates_state(self, auth_client, entry):
        """If should_save is true, create the corresponding state object."""
        assert not EntryState.objects.filter(
            user=get_user(auth_client), state=EntryState.STATE_SAVED, entry=entry
        ).exists()
        url = self._get_save_url(entry)
        auth_client.get(url)
        assert EntryState.objects.filter(user=get_user(auth_client), state=EntryState.STATE_SAVED, entry=entry).exists()

    def test_unsave_deletes_state(self, auth_client, entry):
        """If should_save is false, the corresponding state is deleted."""
        user = get_user(auth_client)
        entry.mark_saved(user)
        assert EntryState.objects.filter(user=get_user(auth_client), state=EntryState.STATE_SAVED, entry=entry).exists()
        url = self._get_unsave_url(entry)
        auth_client.get(url)
        assert not EntryState.objects.filter(user=user, state=EntryState.STATE_SAVED, entry=entry).exists()

    def test_redirect_to_feed(self, auth_client, entry):
        """If all goes well, redirect to the feed."""
        url = self._get_save_url(entry)
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("feeds:my_entries")


@pytest.mark.django_db
class TestFeedWatchToggleView:
    def _get_watch_url(self, feed):
        return reverse("feeds:watch", kwargs={"slug": feed.slug})

    def _get_unwatch_url(self, feed):
        return reverse("feeds:unwatch", kwargs={"slug": feed.slug})

    def test_required_kwargs(self):
        """The view requires the `should_save` kwarg."""
        with pytest.raises(ImproperlyConfigured):
            FeedWatchToggleView()

    def test_requires_login(self, client, feed):
        """Must require an authenticated session to access."""
        url = self._get_watch_url(feed)
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={url}"

    def test_object_not_found_404s(self, auth_client, feed):
        """If an object cannot be matched via slugs, return 404."""
        url = self._get_watch_url(feed)
        feed.delete()
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_should_save_creates_state(self, auth_client, feed):
        """If should_save is true, create the corresponding state object."""
        user = get_user(auth_client)
        assert not feed.is_watched_by(user)
        url = self._get_watch_url(feed)
        auth_client.get(url)
        assert feed.is_watched_by(user)

    def test_unsave_deletes_state(self, auth_client, feed):
        """If should_save is false, the corresponding state is deleted."""
        user = get_user(auth_client)
        user.watch(feed)
        assert feed.is_watched_by(user)
        url = self._get_unwatch_url(feed)
        auth_client.get(url)
        assert not feed.is_watched_by(user)

    def test_redirect_to_feed(self, auth_client, feed):
        """If all goes well, redirect to the feed."""
        url = self._get_watch_url(feed)
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("feeds:my_entries")


@pytest.mark.django_db
class TestMyEntriesListView:
    def setup(self):
        self.url = reverse("feeds:my_entries")

    def test_renders(self, auth_client):
        """The view should render."""
        response = auth_client.get(self.url)
        assert response.status_code == 200

    def test_requires_login(self, client):
        """The view requires the user be logged in."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    def test_only_returns_watched_feed_entries(self, auth_client, entry_factory, feed_factory, user):
        """The view should only return entries for watched feeds."""
        watched_feed = feed_factory()
        user.watch(watched_feed)
        unwatched_feed = feed_factory()
        watched_entries = [entry_factory(feed=watched_feed) for _ in range(5)]
        [entry_factory(feed=unwatched_feed) for _ in range(5)]
        response = auth_client.get(self.url)
        assert response.context["page_obj"].object_list == watched_entries


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
        pinned_entries = [entry_state_factory(user=user, state=EntryState.STATE_PINNED).entry for _ in range(5)]
        [entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry for _ in range(5)]
        response = auth_client.get(self.url)
        for entry in pinned_entries:
            assert entry in response.context["page_obj"].object_list


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
        saved_entries = [entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry for _ in range(5)]
        [entry_state_factory(user=user, state=EntryState.STATE_DELETED).entry for _ in range(5)]
        response = auth_client.get(self.url)
        for entry in saved_entries:
            assert entry in response.context["page_obj"].object_list


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

    def test_only_returns_archived_entries(self, auth_client, entry_state_factory, user):
        """The view should only return entries for archived feeds."""
        archived_entries = [entry_state_factory(user=user, state=EntryState.STATE_DELETED).entry for _ in range(5)]
        [entry_state_factory(user=user, state=EntryState.STATE_SAVED).entry for _ in range(5)]
        response = auth_client.get(self.url)
        for entry in archived_entries:
            assert entry in response.context["page_obj"].object_list
