"""A redirect view's sole purpose is to offload the user out of the system."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from feedzero.feeds.models import Entry


class EntryOffloadView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        """Mark the entry as read, then offload to the corresponding link."""
        entry = get_object_or_404(
            Entry, feed__slug=kwargs["feed_slug"], slug=kwargs["entry_slug"]
        )
        entry.mark_read_by(self.request.user)
        return HttpResponseRedirect(entry.link)
