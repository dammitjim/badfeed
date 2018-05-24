from django.urls import path

import badfeed.feeds.views as _views


app_name = "feeds"
urlpatterns = [
    path('', _views.FeedList.as_view(), name='feed_list'),
    path('<int:pk>/', _views.FeedDetail.as_view(), name='feed_detail'),
    path('<int:feed_pk>/entries/', _views.EntryList.as_view(), name='entry_list'),
    path('<int:feed_pk>/entries/<int:pk>/', _views.EntryDetail.as_view(), name='entry_detail'),
]
