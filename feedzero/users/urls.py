from django.urls import include, path

from feedzero.users.views import LogoutView


app_name = "users"
urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("integrations/pocket/", include("feedzero.users.integrations.pocket.urls")),
]
