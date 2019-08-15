from django.urls import path

from feedzero.api import views


app_name = "api"
urlpatterns = [
    path("entries/", views.EntryListView.as_view(), name="entry_list"),
    path(
        "entries/pinned/", views.PinnedEntryListView.as_view(), name="pinned_entry_list"
    ),
    path("entries/<pk>", views.EntryDetailView.as_view(), name="entry_detail"),
    path("feeds/", views.FeedListView.as_view(), name="feed_list"),
    path("states/", views.EntryStateCreationView.as_view(), name="state_create"),
]
