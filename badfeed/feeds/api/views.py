from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from badfeed.feeds.api.serializers import EntryDetailSerializer, FeedEntrySerializer
from badfeed.feeds.models import Entry, Feed


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
        self.request = request
        queryset = self.get_queryset()
        queryset = self.paginate_queryset(queryset)
        data = [self.get_serializer_instance(feed).data for feed in queryset]
        return self.get_paginated_response(data)


class UnreadEntryList(generics.ListAPIView):
    serializer_class = EntryDetailSerializer

    def get_queryset(self):
        """Load all unread entries to be served."""
        qs = Entry.user_state.unread(self.request.user)
        if "after" in self.request.GET:
            qs = qs.filter(pk__lte=self.request.GET["after"])
        return qs


class EntryStateManagerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntryDetailSerializer

    def get_object(self):
        return get_object_or_404(Entry, pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        """Update the state for the object."""
        if "state" not in request.data:
            raise ParseError("Missing intended state parameter")

        instance = self.get_object()
        state = request.data["state"]
        if state == "save":
            instance.mark_saved(self.request.user)
        elif state == "pin":
            instance.mark_pinned(self.request.user)
        else:
            raise ParseError(f"{state} not a supported entry state")

        return Response(status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete the entry for the user."""
        instance = self.get_object()
        instance.mark_deleted(self.request.user)
        return Response(status=HTTP_204_NO_CONTENT)
