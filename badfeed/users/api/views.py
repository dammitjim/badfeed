from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from badfeed.core.utils import rest_message
from badfeed.feeds.exceptions import InvalidStateException
from badfeed.feeds.models import Feed, Entry
from badfeed.feeds.api.serializers import MyFeedSerializer, EntrySerializer, MyEntryDetailSerializer


class MyFeedList(ListAPIView):

    serializer_class = MyFeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(watched_by=self.request.user)

    def patch(self, request, *args, **kwargs):
        feed = get_object_or_404(Feed, pk=request.data.get("feed", None))
        self.request.user.watch(feed, commit=True)
        return rest_message(f"You are now watching {feed.title}", status.HTTP_201_CREATED)


class MyFeedDetail(RetrieveAPIView):
    serializer_class = MyFeedSerializer

    def get_object(self):
        return get_object_or_404(Feed, slug=self.kwargs["slug"], watched_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Delete stops the feed being watched."""
        feed = self.get_object()
        request.user.unwatch(feed, commit=True)
        return rest_message(f"You are no longer watching {feed.title}", status.HTTP_200_OK)


class MyFeedEntryList(ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__slug=self.kwargs["feed_slug"], feed__watched_by=self.request.user)


class MyFeedEntryDetail(RetrieveAPIView):
    serializer_class = MyEntryDetailSerializer

    def get_object(self):
        return get_object_or_404(
            Entry, slug=self.kwargs["slug"], feed__slug=self.kwargs["feed_slug"], feed__watched_by=self.request.user
        )

    def post(self, request, *args, **kwargs):
        """Add to the user state of the entry."""
        entry = self.get_object()
        state = request.data.get("state", None)
        try:
            entry.add_state(state, self.request.user)
        except InvalidStateException:
            return rest_message(f"{state} is not a valid entry state.", status.HTTP_400_BAD_REQUEST)
        response = self.get(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response

    def delete(self, request, *args, **kwargs):
        """Delete a entry state.

        TODO this shouldn't really be here, should be nested resource
        """
        entry = self.get_object()
        state = request.data.get("state", None)
        try:
            entry.remove_state(state, self.request.user)
        except InvalidStateException:
            return rest_message(f"{state} is not a valid entry state.", status.HTTP_400_BAD_REQUEST)
        return rest_message(f"State modified for {entry.title}", status.HTTP_200_OK)


class MyEntryList(ListAPIView):
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__watched_by=self.request.user).order_by("-date_published")
