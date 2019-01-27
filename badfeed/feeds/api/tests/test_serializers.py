from django.urls import reverse
from django.test import RequestFactory
import pytest

from badfeed.feeds.api import serializers
from badfeed.feeds.models import EntryState


@pytest.mark.django_db
class TestEntrySerializer:
    def test_loads_user_states(self, entry, entry_state_factory, user):
        """If logged in, should include the entry states for the user."""
        request = RequestFactory().get(reverse("api_feeds:feeds"))
        request.user = user
        entry_state_factory(entry=entry, state=EntryState.STATE_PINNED)
        srl = serializers.EntrySerializer(entry, context={"request": request})
        assert EntryState.STATE_PINNED in srl.data["states"]

    def test_logged_out_serializes(self, entry, entry_state_factory):
        """If no request in context, should still serialize."""
        entry_state_factory(entry=entry, state=EntryState.STATE_PINNED)
        srl = serializers.EntrySerializer(entry)
        assert srl.data["id"] is not None

    @pytest.mark.parametrize("field", ["title", "link", "slang_date_published"])
    def test_serializes_required_fields(self, field, entry):
        """Should include the fields as required."""
        srl = serializers.EntrySerializer(entry)
        assert field in srl.data
        assert srl.data[field] == getattr(entry, field)
