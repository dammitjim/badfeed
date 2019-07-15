from django.urls import path

from feedzero.feeds.api import views


app_name = "api_feeds"
urlpatterns = [
    path("entries/unread/", views.UnreadEntryList.as_view(), name="entries_unread"),
    path("dash/", views.GenericFeedDashboardView.as_view(), name="dash"),
    path("state/", views.EntryStateCreationView.as_view(), name="state"),
]

# get unread feeds, 5 per
# done with multiple feeds at once
