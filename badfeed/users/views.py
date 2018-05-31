from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView

from badfeed.core.utils import rest_message
from badfeed.feeds.models import Feed
from badfeed.feeds.serializers import FeedSerializer


class WatchedFeedsList(ListAPIView):

    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(watched_by=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            feed = Feed.objects.get(pk=request.data["feed"])
        except Feed.DoesNotExist:
            raise Http404
        if self.request.user.watching.filter(pk=feed.pk):
            return rest_message("You are already watching this feed.", status.HTTP_400_BAD_REQUEST)
        self.request.user.watching.add(feed)
        self.request.user.save()
        return rest_message(f"You are now watching {feed.title}", status.HTTP_201_CREATED)
