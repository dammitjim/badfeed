from django.urls import include, path

from badfeed.users import views


app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("integrations/pocket/", include("badfeed.users.integrations.pocket.urls")),
]
