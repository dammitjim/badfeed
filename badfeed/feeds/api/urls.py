from django.urls import path

from badfeed.feeds.api import views


app_name = "api_feeds"
urlpatterns = [
    path("entries/unread/", views.UnreadEntryList.as_view(), name="entries_unread"),
    path("entries/<int:pk>/", views.EntryStateManagerView.as_view(), name="entries_state_manager"),
]
