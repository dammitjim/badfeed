from django.urls import include, path

from feedzero.users import views


app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("integrations/pocket/", include("feedzero.users.integrations.pocket.urls")),
]
