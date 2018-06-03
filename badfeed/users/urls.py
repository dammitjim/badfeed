from django.urls import path

import badfeed.users.views as _views


app_name = "users"
urlpatterns = [
    path("feeds/", _views.MyFeedList.as_view(), name="feed_list"),
    path("feeds/<slug:slug>/", _views.MyFeedDetail.as_view(), name="feed_detail"),
    path("feeds/<slug:feed_slug>/entries/", _views.MyFeedEntryList.as_view(), name="feed_entry_list"),
    path("feeds/<slug:feed_slug>/entries/<slug:slug>/", _views.MyFeedEntryDetail.as_view(), name="feed_entry_detail"),
    path("entries/", _views.MyEntryList.as_view(), name="entry_list"),
]
