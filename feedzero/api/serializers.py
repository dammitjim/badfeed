from rest_framework.serializers import ModelSerializer, SerializerMethodField

from feedzero.feeds.models import Entry, EntryState, Feed


class FeedSerializer(ModelSerializer):
    unread = SerializerMethodField()

    def get_unread(self, obj):
        """If appropriate, return the amount of unread entries for the feed."""
        if "request" not in self.context:
            return None

        user = self.context["request"].user
        if not obj.is_watched_by(user):
            return None

        return Entry.user_state.unread(user).filter(feed=obj).count()

    class Meta:
        model = Feed
        fields = ["title", "slug", "link", "date_last_scraped", "unread"]


class EntrySerializer(ModelSerializer):
    feed = FeedSerializer()

    class Meta:
        model = Entry
        fields = ["id", "title", "link", "summary", "guid", "date_published", "feed"]


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


class EntryDetailSerializer(EntrySerializer):
    class Meta:
        model = EntrySerializer.Meta.model
        fields = EntrySerializer.Meta.fields + ["content"]
