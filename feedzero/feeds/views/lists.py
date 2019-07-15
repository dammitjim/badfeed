"""A list view presents a traditional list of content."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from feedzero.feeds.models import Entry, Feed


class InboxView(LoginRequiredMixin, ListView):
    """The primary inbox view, let's get to zero."""

    template_name = "feeds/inbox.html"
    extra_context = {"page_title": "Inbox"}
    paginate_by = 20

    def get_queryset(self):
        return Entry.user_state.unread(self.request.user).order_by("-date_published")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action_entries"] = ctx["object_list"][:3]
        ctx["list_entries"] = ctx["object_list"][3:]
        # TODO this is a bad and will likely shitcan performance
        ctx["remaining"] = len(self.get_queryset())
        return ctx


class FeedInboxView(InboxView):
    feed = None

    def dispatch(self, request, *args, **kwargs):
        self.feed = get_object_or_404(Feed, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(feed=self.feed)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Inbox / {self.feed.title}"
        ctx["feed"] = self.feed
        return ctx


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
