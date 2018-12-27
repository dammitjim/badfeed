from django.urls import path

from badfeed.feeds import views


app_name = "feeds"
urlpatterns = [
    path("search/", views.FeedSearch.as_view(), name="search"),
    path("<slug:slug>/", views.FeedDetailView.as_view(), name="detail"),
    path("<slug:feed_slug>/<slug:entry_slug>/read/", views.EntryOffloadView.as_view(), name="entry_read"),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/pin/", views.EntryPinToggleView.as_view(should_pin=True), name="entry_pin"
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/unpin/",
        views.EntryPinToggleView.as_view(should_pin=False),
        name="entry_unpin",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/save/",
        views.EntrySaveToggleView.as_view(should_save=True),
        name="entry_save",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/unsave/",
        views.EntrySaveToggleView.as_view(should_save=False),
        name="entry_unsave",
    ),
]
