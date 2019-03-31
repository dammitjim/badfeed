"""An action view is one which makes a modification to a set of data, then redirects."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from pocket import Pocket

from badfeed.feeds.forms import EntryActionsForm, FeedActionsForm
from badfeed.feeds.models import Entry, Feed
from badfeed.users.integrations.pocket.views import PocketConsumerKeyMixin
from badfeed.users.models import ThirdPartyTokens


class FeedActionsView(LoginRequiredMixin, FormView):
    form_class = FeedActionsForm
    template_name = "feeds/actions.html"
    success_url = "/"
    object = None

    def dispatch(self, request, *args, **kwargs):
        """We need to ensure that we are performing actions on a feed that exists."""
        self.object = get_object_or_404(Feed, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Perform the appropriate bulk action against the feed."""
        action = form.cleaned_data["action"]
        if action == FeedActionsForm.ACTIONS_ARCHIVE:
            self.object.mark_entries_archived(self.request.user)
        return super().form_valid(form)


class EntryActionsView(LoginRequiredMixin, FormView):
    form_class = EntryActionsForm
    template_name = "feeds/actions.html"
    success_url = "/"
    object = None

    def dispatch(self, request, *args, **kwargs):
        """We need to ensure that we are performing actions on a feed that exists."""
        self.object = get_object_or_404(
            Entry, feed__slug=kwargs["feed_slug"], slug=kwargs["entry_slug"]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Perform the appropriate bulk action against the feed."""
        action = form.cleaned_data["action"]
        if action == EntryActionsForm.ACTIONS_ARCHIVE:
            self.object.archive_older_than_this(self.request.user)
        return super().form_valid(form)


class ObjectActionToggleView(LoginRequiredMixin, View):
    """DRY base class for toggle flags on models on and off."""

    should_toggle = False

    def get_object(self, *args, **kwargs):
        """Return a django model instance."""
        raise NotImplementedError()

    def get_success_url(self):
        """Redirect target after action."""
        return self.request.META.get("HTTP_REFERER", "/")

    def toggle_on(self, obj):
        """Positive, toggle "on" action"""
        raise NotImplementedError()

    def toggle_off(self, obj):
        """Negative, toggle "off" action"""
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        """Load the object, perform appropriate toggle action and redirect."""
        obj = self.get_object(*args, **kwargs)
        if self.should_toggle:
            self.toggle_on(obj)
        else:
            self.toggle_off(obj)
        return redirect(self.get_success_url())

    def __init__(self, *args, **kwargs):
        """Adds a flag signifying if this view toggle.

        This is done to allow the same view be used across two different URLs, with the
        difference being the business logic.
        """
        super().__init__(*args, **kwargs)
        if "should_toggle" not in kwargs:
            raise ImproperlyConfigured("should_toggle is a required parameter")
        self.should_watch = kwargs["should_toggle"]


class EntryDeleteToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_deleted(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_undeleted(self.request.user)


class FeedWatchToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Feed:
        feed_slug = kwargs["slug"]
        return get_object_or_404(Feed, slug=feed_slug)

    def toggle_on(self, obj: Feed):
        self.request.user.watch(obj)

    def toggle_off(self, obj: Feed):
        self.request.user.unwatch(obj)


class EntryPinToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_pinned(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_unpinned(self.request.user)


class EntrySaveToggleView(ObjectActionToggleView):
    def get_object(self, *args, **kwargs) -> Entry:
        feed_slug = kwargs["feed_slug"]
        return get_object_or_404(Entry, feed__slug=feed_slug, slug=kwargs["entry_slug"])

    def toggle_on(self, obj: Entry):
        obj.mark_saved(self.request.user)

    def toggle_off(self, obj: Entry):
        obj.mark_unsaved(self.request.user)


class MultiEntryDeleteView(LoginRequiredMixin, View):
    """To be killed once past proof of concept stage... or maybe not."""

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Delete the entries for the logged in user."""
        ids = request.POST.getlist("to_delete")
        if len(ids) == 0:
            raise SuspiciousOperation()
        entries = Entry.objects.filter(pk__in=ids)
        for entry in entries:
            entry.mark_deleted(self.request.user)
        messages.success(request, f"Deleted {entries.count()} entries.")
        return redirect(self.request.META.get("HTTP_REFERER", "/"))


class SaveEntryToPocketView(LoginRequiredMixin, PocketConsumerKeyMixin, View):
    def get(self, request, *args, **kwargs):
        """Save the given entry to the request user's pocket account."""
        try:
            pocket = Pocket(self.consumer_key, request.user.pocket_token)
        except ThirdPartyTokens.DoesNotExist:
            return redirect(reverse("users:pocket:oauth_entry"))

        entry = get_object_or_404(
            Entry, slug=kwargs["entry_slug"], feed__slug=kwargs["feed_slug"]
        )
        # TODO handle pocket errors for fault tolerance
        pocket.add(entry.link, wait=False)
        entry.mark_saved(request.user)
        return redirect(request.META.get("HTTP_REFERER", "/"))
