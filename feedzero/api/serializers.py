from rest_framework.serializers import ModelSerializer, SerializerMethodField

from feedzero.feeds.models import Entry, EntryState, Feed


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = ["title", "slug", "link", "date_last_scraped"]


class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        fields = ["title", "link", "guid", "date_published", "feed"]


class EntryStateSerializer(ModelSerializer):
    class Meta:
        model = EntryState
        fields = ["state", "date_created"]


class EntryWithStateSerializer(EntrySerializer):
    states = SerializerMethodField()

    def get_states(self, obj):
        """Load entry states for the request user if present."""
        if "request" not in self.context:
            return []

        user = self.context["request"].user
        return [
            EntryStateSerializer(state).data
            for state in EntryState.objects.filter(user=user, entry=obj)
        ]

    class Meta:
        fields = EntrySerializer.Meta.fields + ["states"]
        model = EntrySerializer.Meta.model
