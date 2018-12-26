from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic import FormView

from badfeed.users.forms import RegistrationForm


class PasswordResetView(auth_views.PasswordResetView):
    """Custom reset view as we don't want a dedicated reset done page."""

    # TODO replace with dashboard when it's been made
    success_url = "/"
    template_name = "users/reset_password.html"

    def form_valid(self, form):
        """Post a message stating success."""
        messages.success(self.request, self.Messages.RESET_SUCCESS_MESSAGE)
        return super().form_valid(form)

    class Messages:
        RESET_SUCCESS_MESSAGE = "Your password has been successfully reset."


class PasswordChangeView(auth_views.PasswordChangeView):
    """Custom password change view as we don't want a dedicated change done page."""

    # TODO replace with dashboard when it's been made
    success_url = "/"
    template_name = "users/change_password.html"

    def form_valid(self, form):
        """Post a message stating success."""
        messages.success(self.request, self.Messages.CHANGE_SUCCESS_MESSAGE)
        return super().form_valid(form)

    class Messages:
        CHANGE_SUCCESS_MESSAGE = "Your password has been successfully changed."


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegistrationForm
