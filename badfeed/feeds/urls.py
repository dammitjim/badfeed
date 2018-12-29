from django.urls import path

from badfeed.feeds import views

# TODO these url patterns may need refactoring at some point

app_name = "feeds"
urlpatterns = [
    path("", views.MyEntriesListView.as_view(), name="my_entries"),
    path("search/", views.FeedSearch.as_view(), name="search"),
    path("<slug:slug>/", views.FeedDetailView.as_view(), name="detail"),
    path("<slug:slug>/watch/", views.FeedWatchToggleView.as_view(should_toggle=True), name="watch"),
    path("<slug:slug>/unwatch/", views.FeedWatchToggleView.as_view(should_toggle=False), name="unwatch"),
    path("<slug:feed_slug>/<slug:entry_slug>/read/", views.EntryOffloadView.as_view(), name="entry_read"),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/pin/",
        views.EntryPinToggleView.as_view(should_toggle=True),
        name="entry_pin",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/unpin/",
        views.EntryPinToggleView.as_view(should_toggle=False),
        name="entry_unpin",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/save/",
        views.EntrySaveToggleView.as_view(should_toggle=True),
        name="entry_save",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/unsave/",
        views.EntrySaveToggleView.as_view(should_toggle=False),
        name="entry_unsave",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/delete/",
        views.EntryDeleteToggleView.as_view(should_toggle=True),
        name="entry_delete",
    ),
    path(
        "<slug:feed_slug>/<slug:entry_slug>/undelete/",
        views.EntryDeleteToggleView.as_view(should_toggle=False),
        name="entry_undelete",
    ),
]
