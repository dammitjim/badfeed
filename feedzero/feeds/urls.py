from django.urls import path

from feedzero.feeds.views import InboxView


app_name = "feeds"
urlpatterns = [path("", InboxView.as_view(), name="inbox")]
