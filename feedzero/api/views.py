from rest_framework.exceptions import ParseError, NotFound
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from feedzero.api.serializers import EntrySerializer, EntryWithStateSerializer
from feedzero.feeds.models import Entry, EntryState
from feedzero.feeds.utils import apply_state_to_entry


class EntryListView(ListAPIView):
    """List all unread entries for the request user."""

    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.user_state.unread(self.request.user).order_by("-date_published")


class PinnedEntryListView(ListAPIView):
    """List all current pinned entries for the request user."""

    serializer_class = EntryWithStateSerializer

    def get_queryset(self):
        return Entry.user_state.pinned(self.request.user).order_by(
            "-states__date_created"
        )


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
