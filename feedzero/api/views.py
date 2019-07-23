from rest_framework.exceptions import ParseError, NotFound
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from feedzero.api.serializers import EntrySerializer, EntryWithStateSerializer
from feedzero.feeds.models import Entry, EntryState


class EntryListView(ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.user_state.unread(self.request.user).order_by("-date_published")


class PinnedEntryListView(ListAPIView):
    serializer_class = EntryWithStateSerializer

    def get_queryset(self):
        return Entry.user_state.pinned(self.request.user).order_by(
            "-states__date_created"
        )


class EntryStateCreationView(APIView):
    """Manage multiple state amends simultaneously."""

    def _get_entry(self, entry_id):
        try:
            return Entry.objects.get(pk=entry_id)
        except Entry.DoesNotExist:
            raise NotFound("entry corresponding to entry_id does not exist")

    def _validate_action(self, action: dict):
        if "state" not in action:
            raise ParseError("state is a required parameter of each action")
        if "entry_id" not in action:
            raise ParseError("entry_id is a required parameter of each action")

        valid_states = dict(EntryState.STATE_CHOICES).keys()
        if action["state"] not in valid_states:
            raise ParseError(f"{action['state']} is not a valid state")

    def _apply_action(self, action: dict):
        """Apply the corresponding change against the entry."""
        entry = self._get_entry(action["entry_id"])
        desired_state = action["state"]
        if desired_state == EntryState.STATE_READ:
            entry.mark_read_by(self.request.user)
        elif desired_state == EntryState.STATE_SAVED:
            entry.mark_saved(self.request.user)
        elif desired_state == EntryState.STATE_PINNED:
            entry.mark_pinned(self.request.user)
        elif desired_state == EntryState.STATE_DELETED:
            entry.mark_deleted(self.request.user)

    def post(self, request: Request, format=None):
        """Accept an array of state changes."""
        if "actions" not in request.data:
            raise ParseError("No actions supplied")

        # TODO at some point may want this to continue even if one of them fails
        for action in request.data["actions"]:
            self._validate_action(action)
            self._apply_action(action)

        return Response(status=200)
