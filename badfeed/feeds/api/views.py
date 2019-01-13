from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.exceptions import ParseError

from badfeed.feeds.models import Entry
from badfeed.feeds.api.serializers import EntrySerializer


class UnreadEntryList(generics.ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        """Load all unread entries to be served."""
        return Entry.user_state.unread(self.request.user)


class EntryStateManagerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntrySerializer

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
