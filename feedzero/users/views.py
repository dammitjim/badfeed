from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views import View


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        """Redirect through to auth0 logout."""
        logout(request)
        return_to = urlencode({"returnTo": request.build_absolute_uri("/")})
        logout_url = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/v2/logout?client_id={settings.SOCIAL_AUTH_AUTH0_KEY}&{return_to}"  # noqa
        return redirect(logout_url)
