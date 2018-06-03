from rest_framework.serializers import ModelSerializer

import badfeed.feeds.models as _models


class FeedSerializer(ModelSerializer):
    class Meta:
        model = _models.Feed
        fields = "__all__"


class EntrySerializer(ModelSerializer):
    class Meta:
        model = _models.Entry
        fields = ["id", "slug", "title", "link", "content", "summary", "date_published", "feed"]


class EntryDetailSerializer(EntrySerializer):
    class Meta:
        model = EntrySerializer.Meta.model
        fields = EntrySerializer.Meta.fields + ["author", "contributors", "tags"]
