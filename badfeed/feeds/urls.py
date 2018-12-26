from django.urls import path

from badfeed.feeds import views


app_name = "feeds"
urlpatterns = [
    path("search/", views.FeedSearch.as_view(), name="search"),
    path("<slug:slug>/", views.FeedDetail.as_view(), name="detail"),
    path("<slug:feed_slug>/<slug:entry_slug>/read/", views.EntryDetail.as_view(), name="entry"),
]
