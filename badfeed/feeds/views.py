from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from pocket import Pocket

from badfeed.core.utils import get_spaffy_quote
from badfeed.feeds.models import Entry, Feed
from badfeed.feeds.utils import feeds_by_last_updated_entry, get_actionable_entries
from badfeed.users.integrations.pocket.views import PocketConsumerKeyMixin
from badfeed.users.models import ThirdPartyTokens


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
        entry = get_object_or_404(
            Entry, feed__slug=kwargs["feed_slug"], slug=kwargs["entry_slug"]
        )
        entry.mark_read_by(self.request.user)
        return HttpResponseRedirect(entry.link)


class MultiDeleteView(LoginRequiredMixin, View):
    """To be killed once past proof of concept stage... or maybe not."""

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Delete the entries for the logged in user."""
        ids = request.POST.getlist("to_delete")
        if len(ids) == 0:
            raise SuspiciousOperation()
        entries = Entry.objects.filter(pk__in=ids)
        for entry in entries:
            entry.mark_deleted(self.request.user)
        messages.success(request, f"Deleted {entries.count()} entries.")
        return redirect(self.request.META.get("HTTP_REFERER", "/"))


class ObjectActionToggleView(LoginRequiredMixin, View):
    """DRY base class for toggle flags on models on and off."""

    should_toggle = False

    def get_object(self, *args, **kwargs):
        """Return a django model instance."""
        raise NotImplementedError()

    def get_success_url(self):
        """Redirect target after action."""
        return self.request.META.get("HTTP_REFERER", "/")

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


class DashboardView(LoginRequiredMixin, TemplateView):
    """Render dashboard view until a SPA solution is found."""

    paginate_by = 2
    template_name = "feeds/dashboard.html"
    extra_context = {"page_title": "Inbox"}

    def get_blocks(self, page=1, num_entries=3):
        """Load `num` blocks for the dashboard.

        A block is a feed with it's corresponding, actionable entries.
        """
        page = page - 1  # 0 index it
        feeds = feeds_by_last_updated_entry(self.request.user)
        paginated_slice = feeds[page : page + self.paginate_by]

        return [
            {
                "feed": feed,
                "entries": get_actionable_entries(
                    feed, self.request.user, num=num_entries
                ),
            }
            for feed in paginated_slice
        ]

    def get_context_data(self, **kwargs):
        """Load paginated blocks based on GET parameter for page."""
        context = super().get_context_data(**kwargs)
        context["blocks"] = self.get_blocks(int(self.request.GET.get("page", 1)))
        context["page_subtitle"] = get_spaffy_quote()
        return context


class PinnedEntriesListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = "feeds/list.html"
    model = Entry
    extra_context = {"page_title": "Pinned"}

    def get_queryset(self):
        """Load all pinned entries for the user."""
        return Entry.user_state.pinned(self.request.user).order_by(
            "-states__date_created"
        )


class SavedEntriesListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = "feeds/list.html"
    model = Entry
    extra_context = {"page_title": "Saved"}

    def get_queryset(self):
        """Load all pinned entries for the user."""
        return Entry.user_state.saved(self.request.user).order_by(
            "-states__date_created"
        )


class ArchivedEntriesListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = "feeds/list.html"
    model = Entry
    extra_context = {"page_title": "Archived"}

    def get_queryset(self):
        """Load all pinned entries for the user."""
        return Entry.user_state.deleted(self.request.user).order_by(
            "-states__date_created"
        )


class SaveEntryToPocketView(LoginRequiredMixin, PocketConsumerKeyMixin, View):
    def get(self, request, *args, **kwargs):
        """Save the given entry to the request user's pocket account."""
        try:
            pocket = Pocket(self.consumer_key, request.user.pocket_token)
        except ThirdPartyTokens.DoesNotExist:
            return redirect(reverse("users:pocket:oauth_entry"))

        entry = get_object_or_404(
            Entry, slug=kwargs["entry_slug"], feed__slug=kwargs["feed_slug"]
        )
        # TODO handle pocket errors for fault tolerance
        pocket.add(entry.link, wait=False)
        entry.mark_saved(request.user)
        return redirect(request.META.get("HTTP_REFERER", "/"))
