from django.urls import path

from feedzero.feeds import views


app_name = "feeds"
urlpatterns = [
    path("", views.InboxView.as_view(), name="inbox"),
    path("feeds/add/", views.FeedAddView.as_view(), name="add"),
]
