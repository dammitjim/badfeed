from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View

from badfeed.feeds.models import Feed, Entry


class FeedSearch(LoginRequiredMixin, ListView):
    template_name = "feeds/search.html"

    def dispatch(self, request, *args, **kwargs):
        """Term is a required arg for the search view."""
        if "term" not in request.GET:
            return HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return feeds that match the term."""
        return Feed.objects.filter(title__icontains=self.request.GET["term"])

    def get_context_data(self, **kwargs):
        """Load the search term into the context."""
        ctx = super().get_context_data(**kwargs)
        return {"search_term": self.request.GET["term"], **ctx}


class FeedDetailView(LoginRequiredMixin, DetailView):
    model = Feed
    template_name = "feeds/detail.html"


class EntryOffloadView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        """Mark the entry as read, then offload to the corresponding link."""
        entry = get_object_or_404(Entry, feed__slug=kwargs["feed_slug"], slug=kwargs["entry_slug"])
        entry.mark_read_by(self.request.user)
        return HttpResponseRedirect(entry.link)


class ObjectActionToggleView(LoginRequiredMixin, View):
    """DRY base class for toggle flags on models on and off."""

    should_toggle = False

    def get_object(self, *args, **kwargs):
        """Return a django model instance."""
        raise NotImplementedError()

    def get_success_url(self):
        """Redirect target after action."""
        return reverse("feeds:my_entries")

    def toggle_on(self, obj):
        """Positive, toggle "on" action"""
        raise NotImplementedError()

    def toggle_off(self, obj):
        """Negative, toggle "off" action"""
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        """Load the object, perform appropriate toggle action and redirect."""
        obj = self.get_object(*args, **kwargs)
        if self.should_toggle:
            self.toggle_on(obj)
        else:
            self.toggle_off(obj)
        return redirect(self.get_success_url())

    def __init__(self, *args, **kwargs):
        """Adds a flag signifying if this view toggle.

        This is done to allow the same view be used across two different URLs, with the
        difference being the business logic.
        """
        super().__init__(*args, **kwargs)
        if "should_toggle" not in kwargs:
            raise ImproperlyConfigured("should_toggle is a required parameter")
        self.should_watch = kwargs["should_toggle"]


class EntryDeleteToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_deleted(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_undeleted(self.request.user)


class FeedWatchToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Feed:
        feed_slug = kwargs["slug"]
        return get_object_or_404(Feed, slug=feed_slug)

    def toggle_on(self, obj: Feed):
        self.request.user.watch(obj)

    def toggle_off(self, obj: Feed):
        self.request.user.unwatch(obj)


class EntryPinToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_pinned(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_unpinned(self.request.user)


class EntrySaveToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_saved(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_unsaved(self.request.user)


class MyEntriesListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = "feeds/my_entries.html"
    model = Entry

    def get_queryset(self):
        """Load all entries for the the feeds watched by the user."""
        feeds = Feed.objects.watched_by(self.request.user)
        entries = Entry.objects.filter(feed__in=feeds).exclude(states__isnull=False)
        return entries.order_by("-date_published")
