from django.urls import path

import badfeed.users.views as _views


app_name = "users"
urlpatterns = [path("feeds/", _views.WatchedFeedsList.as_view(), name="watched_feeds")]
