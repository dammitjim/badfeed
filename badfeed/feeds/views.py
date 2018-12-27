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
        entry = get_object_or_404(Entry, feed__slug=kwargs["feed_slug"], slug=kwargs["entry_slug"])
        entry.mark_read_by(self.request.user)
        return HttpResponseRedirect(entry.link)


class EntryPin(LoginRequiredMixin, View):
    should_pin = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_pin = kwargs["should_pin"]

    def dispatch(self, request, *args, **kwargs):
        feed_slug = kwargs["feed_slug"]
        entry = get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

        if self.should_pin:
            entry.mark_pinned(request.user)
        else:
            entry.mark_unpinned(request.user)

        redirect_url = reverse("feeds:detail", kwargs={"slug": feed_slug})
        return redirect(redirect_url)


class EntrySave(LoginRequiredMixin, View):
    should_save = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_save = kwargs["should_save"]

    def dispatch(self, request, *args, **kwargs):
        feed_slug = kwargs["feed_slug"]
        entry = get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

        if self.should_save:
            entry.mark_saved(request.user)
        else:
            entry.mark_unsaved(request.user)

        redirect_url = reverse("feeds:detail", kwargs={"slug": feed_slug})
        return redirect(redirect_url)
