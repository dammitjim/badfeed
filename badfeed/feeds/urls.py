from django.urls import path

from badfeed.feeds.views import FeedSearch


app_name = "feeds"
urlpatterns = [path("search/", FeedSearch.as_view(), name="search")]
