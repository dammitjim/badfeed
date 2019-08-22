from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class InboxView(LoginRequiredMixin, TemplateView):
    """The primary inbox view, let's get to zero."""

    template_name = "feeds/inbox.html"
