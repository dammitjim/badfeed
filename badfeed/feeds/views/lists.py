"""A list view presents a traditional list of content."""
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from badfeed.feeds.models import Entry, Feed
from badfeed.feeds.utils import feeds_by_last_updated_entry, get_actionable_entries


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


class DashboardView(LoginRequiredMixin, TemplateView):
    """Render dashboard view until a SPA solution is found."""

    PAGINATE_BY = 2
    template_name = "feeds/dashboard.html"
    extra_context = {"page_title": "Inbox"}

    def get_context_data(self, **kwargs):
        """Load paginated blocks based on GET parameter for page."""
        context = super().get_context_data(**kwargs)
        context["blocks"] = self.get_blocks(int(self.request.GET.get("page", 1)))
        return context

    def get_blocks(self, page: int):
        """Load blocks for the dashboard.

        A block is a feed with it's corresponding, actionable entries.
        """
        feeds = feeds_by_last_updated_entry(self.request.user)
        paginated_feeds = self._paginate_feeds(feeds, page)
        blocks = self._build_blocks(paginated_feeds)
        return blocks

    def _paginate_feeds(self, feeds: List[Feed], page: int):
        """Get the appropriate slice of feeds for the given page.

        The page argument should not be 0 indexed, it should instead be the human
        interpreted version. This is because we 0 index it as a part of the function.
        """
        page = page - 1
        paginated_slice = feeds[page : page + self.PAGINATE_BY]
        return paginated_slice

    def _build_blocks(self, paginated_feeds: List[Feed], entries_per_block: int = 3):
        """Construct a list of blocks containing the actionable entries for the given feeds"""
        blocks = []
        for feed in paginated_feeds:
            actionable_entries = get_actionable_entries(feed, self.request.user)
            blocks.append(
                {
                    "feed": feed,
                    "entries": actionable_entries[:entries_per_block],
                    "total_entries": len(actionable_entries),
                }
            )
        return blocks


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
