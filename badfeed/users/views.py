from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "users/login.html"
    extra_context = {"page_title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        """Redirect already logged in users if they try to be cheeky."""
        if request.user.is_authenticated:
            messages.info(request, self.Messages.ALREADY_LOGGED_IN)
            return redirect(reverse("feeds:inbox"))
        return super().dispatch(request, *args, **kwargs)

    class Messages:
        ALREADY_LOGGED_IN = "You are already logged in."
