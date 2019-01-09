from django.urls import path

from badfeed.users.integrations.pocket import views


app_name = "pocket"
urlpatterns = [
    path("entry/", views.OAuthEntry.as_view(), name="oauth_entry"),
    path("callback/", views.OAuthCallback.as_view(), name="oauth_callback"),
]
