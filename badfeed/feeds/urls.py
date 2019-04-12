from django.urls import path

from badfeed.feeds.views import actions, details, lists, redirects, search

# TODO these url patterns may need refactoring at some point

app_name = "feeds"
urlpatterns = [
    path("", lists.DashboardView.as_view(), name="my_entries"),
    path("inbox/", lists.InboxView.as_view(), name="inbox"),
    path("search/", search.FeedSearch.as_view(), name="search"),
    path("pinned/", lists.PinnedEntriesListView.as_view(), name="pinned_entries"),
    path("saved/", lists.SavedEntriesListView.as_view(), name="saved_entries"),
    path("archived/", lists.ArchivedEntriesListView.as_view(), name="archived_entries"),
    path("f/<slug:slug>/", details.FeedDetailView.as_view(), name="detail"),
    path(
        "f/<slug:feed_slug>/<slug:entry_slug>/",
        details.EntryDetailView.as_view(),
        name="entry_detail",
    ),
]

# TODO put some thought into these urls as they ain't great
action_urls = [
    path("fa/<slug:slug>/actions/", actions.FeedActionsView.as_view(), name="actions"),
    path(
        "fa/<slug:slug>/watch/",
        actions.FeedWatchToggleView.as_view(should_toggle=True),
        name="watch",
    ),
    path(
        "fa/<slug:slug>/unwatch/",
        actions.FeedWatchToggleView.as_view(should_toggle=False),
        name="unwatch",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/read/",
        redirects.EntryOffloadView.as_view(),
        name="entry_read",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/pin/",
        actions.EntryPinToggleView.as_view(should_toggle=True),
        name="entry_pin",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/unpin/",
        actions.EntryPinToggleView.as_view(should_toggle=False),
        name="entry_unpin",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/save/",
        actions.EntrySaveToggleView.as_view(should_toggle=True),
        name="entry_save",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/unsave/",
        actions.EntrySaveToggleView.as_view(should_toggle=False),
        name="entry_unsave",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/delete/",
        actions.EntryDeleteToggleView.as_view(should_toggle=True),
        name="entry_delete",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/undelete/",
        actions.EntryDeleteToggleView.as_view(should_toggle=False),
        name="entry_undelete",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/actions/",
        actions.EntryActionsView.as_view(),
        name="entry_actions",
    ),
    path(
        "fa/<slug:feed_slug>/<slug:entry_slug>/pocket/",
        actions.SaveEntryToPocketView.as_view(),
        name="entry_pocket",
    ),
    path(
        "delete-multi/",
        actions.MultiEntryDeleteView.as_view(),
        name="entry_multi_delete",
    ),
]

urlpatterns += action_urls
