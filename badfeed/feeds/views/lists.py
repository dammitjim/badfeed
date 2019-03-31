"""A list view presents a traditional list of content."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from badfeed.core.utils import get_spaffy_quote
from badfeed.feeds.models import Entry
from badfeed.feeds.utils import feeds_by_last_updated_entry, get_actionable_entries


class DashboardView(LoginRequiredMixin, TemplateView):
    """Render dashboard view until a SPA solution is found."""

    paginate_by = 2
    template_name = "feeds/dashboard.html"
    extra_context = {"page_title": "Inbox"}

    def get_blocks(self, page=1, entries_per_block=3):
        """Load `num` blocks for the dashboard.

        A block is a feed with it's corresponding, actionable entries.
        """
        page = page - 1  # 0 index it
        feeds = feeds_by_last_updated_entry(self.request.user)
        paginated_slice = feeds[page : page + self.paginate_by]

        blocks = []
        for feed in paginated_slice:
            actionable_entries = get_actionable_entries(feed, self.request.user)
            blocks.append(
                {
                    "feed": feed,
                    "entries": actionable_entries[:entries_per_block],
                    "total_entries": len(actionable_entries),
                }
            )

        return blocks

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
