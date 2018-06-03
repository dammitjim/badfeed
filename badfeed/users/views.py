from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from badfeed.core.utils import rest_message
from badfeed.feeds.models import Feed, Entry
from badfeed.feeds.serializers import FeedSerializer, EntrySerializer


class MyFeedList(ListAPIView):

    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(watched_by=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            feed = Feed.objects.get(pk=request.data["feed"])
        except Feed.DoesNotExist:
            raise Http404
        self.request.user.watch(feed, commit=True)
        return rest_message(f"You are now watching {feed.title}", status.HTTP_201_CREATED)


class MyFeedDetail(RetrieveAPIView):
    serializer_class = FeedSerializer

    def get_object(self):
        return get_object_or_404(Feed, slug=self.kwargs["slug"], watched_by=self.request.user)


class MyFeedEntryList(ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__slug=self.kwargs["feed_slug"], feed__watched_by=self.request.user)


class MyFeedEntryDetail(RetrieveAPIView):
    serializer_class = EntrySerializer

    def get_object(self):
        return get_object_or_404(
            Entry, slug=self.kwargs["slug"], feed__slug=self.kwargs["feed_slug"], feed__watched_by=self.request.user
        )


class MyEntryList(ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__watched_by=self.request.user)
