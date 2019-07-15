from django.test import RequestFactory
from django.urls import reverse
import pytest

from feedzero.feeds.api import serializers
from feedzero.feeds.models import EntryState


@pytest.mark.django_db
class TestEntrySerializer:
    def test_loads_user_states(self, entry, entry_state_factory, user):
        """If logged in, should include the entry states for the user."""
        request = RequestFactory().get(reverse("api_feeds:dash"))
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

    def test_serializes_feed(self, entry):
        """Should serialize the associated feed."""
        srl = serializers.EntrySerializer(entry)
        feed = srl.data["feed"]
        assert entry.feed.title == feed["title"]


@pytest.mark.django_db
class TestFeedEntrySerializer:
    def test_omits_nested_feed_serialization(self, feed, entry_factory):
        """Should not serialize the feed nested in entry as we have it at top level."""
        entry_1 = entry_factory(feed=feed)
        entry_2 = entry_factory(feed=feed)
        srl = serializers.FeedEntrySerializer(
            {"feed": feed, "entries": [entry_1, entry_2]}
        )
        assert "feed" not in srl.data["entries"][0]
