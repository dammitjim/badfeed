from rest_framework.exceptions import ParseError, NotFound
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from feedzero.api.filters import FeedListFilterSet
from feedzero.api.serializers import (
    EntrySerializer,
    EntryDetailSerializer,
    EntryWithStateSerializer,
    FeedSerializer,
)
from feedzero.feeds.models import Entry, EntryState, Feed
from feedzero.feeds.utils import apply_state_to_entry


class EntryListView(ListAPIView):
    """List all unread entries for the request user."""

    serializer_class = EntrySerializer
    filterset_fields = ["feed"]

    def get_queryset(self):
        return Entry.user_state.unread(self.request.user).order_by("-date_published")


class PinnedEntryListView(ListAPIView):
    """List all current pinned entries for the request user."""

    serializer_class = EntryWithStateSerializer

    def get_queryset(self):
        return Entry.user_state.pinned(self.request.user).order_by(
            "-states__date_created"
        )


class EntryDetailView(RetrieveAPIView):
    """Detail view for an individual entry."""

    serializer_class = EntryDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class FeedListView(ListAPIView):
    """Listing view for feeds."""

    serializer_class = FeedSerializer
    filterset_class = FeedListFilterSet

    def get_queryset(self):
        only = self.request.GET.get("only", None)
        if only == "user":
            return Feed.objects.watched_by(self.request.user)
        return Feed.objects.all()


class EntryStateCreationView(APIView):
    """Manage multiple state amends simultaneously."""

    def __init__(self):
        super().__init__()
        self.valid_states = dict(EntryState.STATE_CHOICES).keys()

    def _get_entry(self, entry_id):
        try:
            return Entry.objects.get(pk=entry_id)
        except Entry.DoesNotExist:
            raise NotFound("entry corresponding to entry_id does not exist")

    def validate_action(self, action: dict):
        if "state" not in action:
            raise ParseError("state is a required parameter of each action")
        if "entry_id" not in action:
            raise ParseError("entry_id is a required parameter of each action")

        if action["state"] not in self.valid_states:
            raise ParseError(f"{action['state']} is not a valid state")

    def post(self, request: Request, format=None):
        """Accept an array of state changes."""
        if "actions" not in request.data:
            raise ParseError("No actions supplied")

        # TODO at some point may want this to continue even if one of them fails
        for action in request.data["actions"]:
            self.validate_action(action)

            try:
                entry_id = action["entry_id"]
                entry = Entry.objects.get(pk=entry_id)
            except Entry.DoesNotExist:
                raise NotFound("entry corresponding to entry_id does not exist")

            desired_state = action["state"]
            apply_state_to_entry(entry, desired_state, self.request.user)

        return Response(status=200)
