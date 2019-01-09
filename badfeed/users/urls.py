from django.urls import path, include

from badfeed.users import views


app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("reset-password/", views.PasswordResetView.as_view(), name="password_reset"),
    path("change-password/", views.PasswordChangeView.as_view(), name="password_change"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("integrations/pocket/", include("badfeed.users.integrations.pocket.urls")),
]
