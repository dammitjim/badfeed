from django.db.models import Count
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from badfeed.feeds.api.serializers import (
    EntryDetailSerializer,
    EntrySerializer,
    FeedEntrySerializer,
)
from badfeed.feeds.models import Entry, EntryState, Feed


class GenericFeedDashboardView(generics.ListAPIView):
    serializer_class = FeedEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Load watched feeds, ordered by when their entries were last published.

        The query we return must match the following conditions:

        * The feed must have 1 or more entries
        * The feed must have 1 or more unread entries for this user
            where an unread entry is one without a state
        * The entries must be ordered by date published
        * Fully actioned feeds must not be returned.

        TODO there is probably a nicer way of writing this queryset chain
        """
        return (
            Feed.objects.watched_by(self.request.user)
            .filter(entries__gt=0)
            .filter(entries__states__isnull=True)
            .annotate(entry_states=Count("entries__states"))
            .filter(entry_states__gte=0)
            .order_by("-entries__date_published")
        )

    def get_serializer_instance(self, feed):
        """Load the 5 latest unread entries for the given feed into a serializer instance."""
        unread_entries = (
            feed.entries(manager="user_state")
            .unread(self.request.user)
            .order_by("-date_published")
        )
        unread_entries = unread_entries[:5]
        return FeedEntrySerializer(
            instance={"feed": feed, "entries": unread_entries},
            context=self.get_serializer_context(),
        )

    def list(self, request, *args, **kwargs):
        """Render a paginated list of watched feeds, with 5 unread entries each."""
        queryset = self.get_queryset()
        queryset = self.paginate_queryset(queryset)
        data = [self.get_serializer_instance(feed).data for feed in queryset]
        return self.get_paginated_response(data)


class EntryListView(generics.ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        """Present unread objects first, ordered by date published."""
        return (
            Entry.objects.filter(feed__pk=self.kwargs["feed_pk"])
            .annotate(unread=Count("states"))
            .order_by("-unread", "-date_published")
        )


class EntryStateCreationView(APIView):
    """Manage multiple state amends simultaneously.

    This view in general could be generalised, and could use serializers.
    This will do for now.

    """

    permission_classes = (IsAuthenticated,)

    def _apply(self, action: dict):
        """Validate, then apply state change against matched entry."""
        if "state" not in action:
            raise ParseError("state is a required parameter of each action")
        if "entry_id" not in action:
            raise ParseError("entry_id is a required parameter of each action")

        try:
            entry = Entry.objects.get(pk=action["entry_id"])
        except Entry.DoesNotExist:
            # TODO log?
            return

        desired = action["state"]
        if desired == EntryState.STATE_READ:
            entry.mark_read_by(self.request.user)
        elif desired == EntryState.STATE_SAVED:
            entry.mark_saved(self.request.user)
        elif desired == EntryState.STATE_PINNED:
            entry.mark_pinned(self.request.user)
        elif desired == EntryState.STATE_DELETED:
            entry.mark_deleted(self.request.user)
        else:
            raise ParseError("invalid state provided")

    def post(self, request: Request, format=None):
        """Accept an array of state changes."""
        if "actions" not in request.data:
            raise ParseError("No actions supplied")

        for action in request.data["actions"]:
            self._apply(action)

        return Response(status=200)


class UnreadEntryList(generics.ListAPIView):
    serializer_class = EntryDetailSerializer

    def get_queryset(self):
        """Load all unread entries to be served."""
        qs = Entry.user_state.unread(self.request.user)
        if "after" in self.request.GET:
            qs = qs.filter(pk__lte=self.request.GET["after"])
        return qs
