from django.urls import path

import badfeed.users.api.views as api_views


app_name = "users"
urlpatterns = [
    path("feeds/", api_views.MyFeedList.as_view(), name="feed_list"),
    path("feeds/<slug:slug>/", api_views.MyFeedDetail.as_view(), name="feed_detail"),
    path("feeds/<slug:feed_slug>/entries/", api_views.MyFeedEntryList.as_view(), name="feed_entry_list"),
    path(
        "feeds/<slug:feed_slug>/entries/<slug:slug>/", api_views.MyFeedEntryDetail.as_view(), name="feed_entry_detail"
    ),
    path("entries/", api_views.MyEntryList.as_view(), name="entry_list"),
]
