from rest_framework.serializers import ModelSerializer

import badfeed.feeds.models as _models


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = _models.Author
        fields = ["id", "name", "link", "email"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = _models.Tag
        fields = ["id", "term", "scheme", "label", "feed"]


class EnclosureSerializer(ModelSerializer):
    class Meta:
        model = _models.Enclosure
        fields = ["id", "href", "file_type", "length", "entry"]


class FeedSerializer(ModelSerializer):
    class Meta:
        model = _models.Feed
        fields = ["id", "slug", "title", "link", "date_last_scraped"]


class EntrySerializer(ModelSerializer):

    feed = FeedSerializer()

    class Meta:
        model = _models.Entry
        fields = ["id", "slug", "title", "link", "content", "summary", "date_published", "feed"]


class EntryDetailSerializer(EntrySerializer):

    author = AuthorSerializer()
    contributors = AuthorSerializer(many=True)
    tags = TagSerializer(many=True)
    enclosures = EnclosureSerializer(many=True)

    class Meta:
        model = EntrySerializer.Meta.model
        fields = EntrySerializer.Meta.fields + ["author", "contributors", "tags", "enclosures"]


class EntryStateSerializer(ModelSerializer):
    class Meta:
        model = _models.EntryState
        fields = ["id", "state", "entry"]


class MyEntryDetailSerializer(EntryDetailSerializer):

    states = EntryStateSerializer(many=True)

    class Meta:
        model = EntryDetailSerializer.Meta.model
        fields = EntryDetailSerializer.Meta.fields + ["states"]
