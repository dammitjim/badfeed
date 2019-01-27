from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from badfeed.feeds.models import Entry, Feed
from badfeed.feeds.api.serializers import EntryDetailSerializer, FeedEntrySerializer


class FeedDashboardView(APIView):
    def get(self, request, *args, **kwargs):
        feeds = Feed.objects.watched_by(request.user).order_by(
            "entries__date_published"
        )
        feeds = feeds[:5]

        output = []
        for feed in feeds:
            # get top 5 unread entries, ordered by date published for this feed
            unread_entries = (
                feed.entries(manager="user_state")
                .unread(request.user)
                .order_by("date_published")
            )
            unread_entries = unread_entries[:5]
            serializer = FeedEntrySerializer(
                instance={"feed": feed, "entries": unread_entries}
            )
            output.append(serializer.data)

        return Response(data=output)

    def destroy(self, request, *args, **kwargs):
        pass


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
