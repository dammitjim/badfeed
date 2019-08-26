from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView

from feedzero.feeds.forms import FeedAddForm


class InboxView(LoginRequiredMixin, TemplateView):
    """The primary inbox view, let's get to zero."""

    template_name = "feeds/inbox.html"


class FeedAddView(LoginRequiredMixin, FormView):
    """Used to add feeds to feedzero."""

    form_class = FeedAddForm
    success_url = "/"
    template_name = "feeds/add.html"

    def form_valid(self, form):
        form.insert()
        return super().form_valid(form)
