"""A detail view displays individual content."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from badfeed.feeds.models import Feed


class FeedDetailView(LoginRequiredMixin, DetailView):
    model = Feed
    template_name = "feeds/detail.html"
