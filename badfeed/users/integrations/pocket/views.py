from uuid import uuid4

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from pocket import Pocket


class ConsumerKeyMixin:
    STATE_COOKIE_KEY = "badfeed_pocket_state"
    CODE_COOKIE_KEY = "badfeed_pocket_code"

    def __init__(self, *args, **kwargs):
        """Load the consumer key into the instance variables of the mixin."""
        super().__init__(*args, **kwargs)
        self.consumer_key = settings.POCKET_CONSUMER_KEY


class OAuthEntry(LoginRequiredMixin, ConsumerKeyMixin, View):
    http_method_names = ["get"]

    def __init__(self, *args, **kwargs):
        """Load the state for cross-request validation into instance of class."""
        super().__init__(*args, **kwargs)
        self.state = uuid4()

    def _get_redirect_url(self):
        redirect = reverse("users:pocket:oauth_callback")
        return self.request.build_absolute_uri(redirect)

    def _get_request_token(self) -> str:
        """Retrieve a oauth token from Pocket."""
        return Pocket.get_request_token(
            consumer_key=self.consumer_key, redirect_uri=self._get_redirect_url(), state=self.state
        )

    def _get_auth_url(self, token) -> str:
        """Retrieve the auth url for the token."""
        return Pocket.get_auth_url(code=token, redirect_uri=self._get_redirect_url())

    def get(self, *args, **kwargs):
        """Initialise the OAuth flow for pocket."""
        token = self._get_request_token()
        response = HttpResponseRedirect(self._get_auth_url(token))
        response.set_cookie(self.STATE_COOKIE_KEY, self.state)
        response.set_cookie(self.CODE_COOKIE_KEY, token)
        return response


class OAuthCallback(LoginRequiredMixin, ConsumerKeyMixin, View):
    http_method_names = ["get"]
    success_url = "/"

    def _get_access_token(self, code) -> str:
        """Retrieve the user credentials from pocket."""
        creds = Pocket.get_access_token(self.consumer_key, code)
        return creds

    def _set_access_token_to_user(self):
        """Get the access token from pocket, store it associated to request user."""
        code = self.request.COOKIES[self.CODE_COOKIE_KEY]
        access_token = self._get_access_token(code)
        self.request.user.store_pocket_token(access_token)

    def get(self, *args, **kwargs):
        """Retrieve an access token from pocket, save to user, redirect."""
        self._set_access_token_to_user()

        response = HttpResponseRedirect(self.success_url)
        response.delete_cookie(self.STATE_COOKIE_KEY)
        response.delete_cookie(self.CODE_COOKIE_KEY)
        return response
