from django.urls import path

import badfeed.feeds.views as _views


app_name = "feeds"
urlpatterns = [
    path("", _views.FeedList.as_view(), name="feed_list"),
    path("<int:pk>/", _views.FeedDetailByPK.as_view(), name="feed_detail_by_pk"),
    path("<slug:slug>/", _views.FeedDetailBySlug.as_view(), name="feed_detail_by_slug"),
    path("<int:feed_pk>/entries/", _views.EntryListByPK.as_view(), name="entry_list_by_pk"),
    path("<slug:feed_slug>/entries/", _views.EntryListBySlug.as_view(), name="entry_list_by_slug"),
    path("<int:feed_pk>/entries/<int:pk>/", _views.EntryDetail.as_view(), name="entry_detail"),
]
