from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http.response import HttpResponseNotFound

from badfeed.feeds.models import Feed


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
