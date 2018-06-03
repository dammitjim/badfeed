from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView

import badfeed.feeds.models as _models
import badfeed.feeds.serializers as _serializers


class FeedList(ListAPIView):
    """List of all Feed objects."""

    queryset = _models.Feed.objects.all()
    serializer_class = _serializers.FeedSerializer


class BaseFeedDetail(RetrieveAPIView):
    """Detail of a single Feed object."""

    queryset = _models.Feed.objects.all()
    serializer_class = _serializers.FeedSerializer


class FeedDetailByPK(BaseFeedDetail):
    """Detail of a single Feed object by PK"""

    pass


class FeedDetailBySlug(BaseFeedDetail):
    """Detail of a single Feed object by slug"""

    lookup_field = "slug"


class BaseEntryList(ListAPIView):
    """List of Entry objects for Feed."""

    serializer_class = _serializers.EntrySerializer


class EntryListByPK(BaseEntryList):
    """List of Entry objects for Feed."""

    def get_queryset(self):
        return get_list_or_404(_models.Entry, feed=self.kwargs["feed_pk"])


class EntryListBySlug(BaseEntryList):
    """List of Entry objects for Feed by slug."""

    def get_queryset(self):
        return get_list_or_404(_models.Entry, feed__slug=self.kwargs["feed_slug"])


class EntryDetail(RetrieveAPIView):
    """List of Entry objects for Feed."""

    serializer_class = _serializers.EntryDetailSerializer

    def get_object(self):
        return get_object_or_404(_models.Entry, feed=self.kwargs["feed_pk"], pk=self.kwargs["pk"])
