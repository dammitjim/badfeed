"""A detail view displays individual content."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from badfeed.feeds.models import Entry, Feed


class FeedDetailView(LoginRequiredMixin, DetailView):
    model = Feed
    template_name = "feeds/feed_detail.html"


class EntryDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "entry"
    model = Entry
    template_name = "feeds/entry_detail.html"

    def get_object(self, queryset=None):
        """Load object based on feed and entry slugs."""
        return get_object_or_404(
            Entry, slug=self.kwargs["entry_slug"], feed__slug=self.kwargs["feed_slug"]
        )

    def get_context_data(self, **kwargs):
        """Load page title into context."""
        ctx = super().get_context_data(**kwargs)
        ctx["enriched"] = hasattr(self.object, "enriched")
        ctx["page_title"] = self.object.title
        ctx["page_subtitle"] = f"{self.object.feed.title}"
        return ctx
