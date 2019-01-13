from rest_framework.serializers import ModelSerializer, SerializerMethodField

from badfeed.feeds.models import Entry, Feed, EntryState


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = ["title", "link"]


class EntrySerializer(ModelSerializer):
    feed = FeedSerializer()
    states = SerializerMethodField()

    def get_states(self, obj):
        return [instance.state for instance in EntryState.objects.filter(entry=obj, user=self.context["request"].user)]

    class Meta:
        model = Entry
        fields = ["id", "feed", "title", "link", "content", "summary", "date_published", "states"]
