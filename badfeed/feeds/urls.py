from django.urls import path

from badfeed.feeds import views

# TODO these url patterns may need refactoring at some point

app_name = "feeds"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="my_entries"),
    path("search/", views.FeedSearch.as_view(), name="search"),
    path("pinned/", views.PinnedEntriesListView.as_view(), name="pinned_entries"),
    path("saved/", views.SavedEntriesListView.as_view(), name="saved_entries"),
    path("archived/", views.ArchivedEntriesListView.as_view(), name="archived_entries"),
    path("delete-multi/", views.MultiDeleteView.as_view(), name="entry_multi_delete"),
    path("f/<slug:slug>/", views.FeedDetailView.as_view(), name="detail"),
    path("f/<slug:slug>/actions/", views.FeedActionsView.as_view(), name="actions"),
    path(
        "f/<slug:slug>/watch/",
        views.FeedWatchToggleView.as_view(should_toggle=True),
        name="watch",
    ),
    path(
        "f/<slug:slug>/unwatch/",
        views.FeedWatchToggleView.as_view(should_toggle=False),
        name="unwatch",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/read/",
        views.EntryOffloadView.as_view(),
        name="entry_read",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/pin/",
        views.EntryPinToggleView.as_view(should_toggle=True),
        name="entry_pin",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/unpin/",
        views.EntryPinToggleView.as_view(should_toggle=False),
        name="entry_unpin",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/save/",
        views.EntrySaveToggleView.as_view(should_toggle=True),
        name="entry_save",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/unsave/",
        views.EntrySaveToggleView.as_view(should_toggle=False),
        name="entry_unsave",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/delete/",
        views.EntryDeleteToggleView.as_view(should_toggle=True),
        name="entry_delete",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/undelete/",
        views.EntryDeleteToggleView.as_view(should_toggle=False),
        name="entry_undelete",
    ),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/pocket/",
        views.SaveEntryToPocketView.as_view(),
        name="entry_pocket",
    ),
]
