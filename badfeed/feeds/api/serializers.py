from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
)

from badfeed.feeds.models import Entry, Feed, EntryState


class OmitMixin:
    def __init__(self, *args, **kwargs):
        """Optional kwarg to omit fields from the serialized result."""
        omit = kwargs.pop("omit", None)
        super(OmitMixin, self).__init__(*args, **kwargs)
        if omit is not None:
            # Drop any fields that are not specified in the `fields` argument.
            for field in set(self.fields):
                if field in omit:
                    self.fields.pop(field)


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = ["title", "link"]


class EntrySerializer(OmitMixin, ModelSerializer):
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
    entries = EntrySerializer(many=True, omit=["feed"])
