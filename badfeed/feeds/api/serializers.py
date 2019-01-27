from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
)

from badfeed.feeds.models import Entry, Feed, EntryState


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = ["title", "link"]


class EntrySerializer(ModelSerializer):
    feed = FeedSerializer()
    states = SerializerMethodField()

    def get_states(self, obj):
        """Load entry states for the request user if present."""
        if "request" not in self.context:
            return []

        return [
            instance.state
            for instance in EntryState.objects.filter(
                entry=obj, user=self.context["request"].user
            )
        ]

    class Meta:
        model = Entry
        fields = [
            "id",
            "feed",
            "title",
            "link",
            "content",
            "summary",
            "date_published",
            "slang_date_published",
            "states",
        ]


class EntryDetailSerializer(EntrySerializer):
    feed = FeedSerializer()

    class Meta:
        model = Entry
        fields = EntrySerializer.Meta.fields + ["feed"]


class FeedEntrySerializer(Serializer):
    feed = FeedSerializer()
    entries = EntrySerializer(many=True)
