from uuid import uuid4

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View


class ConsumerKeyMixin:
    STATE_COOKIE_KEY = "badfeed_pocket_state"
    CODE_COOKIE_KEY = "badfeed_pocket_code"

    def __init__(self, *args, **kwargs):
        """Load the consumer key into the instance variables of the mixin."""
        super().__init__(*args, **kwargs)
        self.consumer_key = settings.POCKET_CONSUMER_KEY


class OAuthEntry(LoginRequiredMixin, ConsumerKeyMixin, View):
    OAUTH_REQUEST_URL = "https://getpocket.com/v3/oauth/request"

    http_method_names = ["GET"]

    def get(self, *args, **kwargs):
        state = uuid4()
        redirect_uri = ""
        pkt_response = requests.post(
            self.OAUTH_REQUEST_URL,
            json={"consumer_key": self.consumer_key, "redirect_uri": redirect_uri, "state": state},
        )
        pkt_json = pkt_response.json()
        request_token = pkt_json["code"]
        user_auth_url = (
            f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={redirect_uri}"
        )
        response = HttpResponseRedirect(user_auth_url)
        response.set_cookie(self.STATE_COOKIE_KEY, state)
        response.set_cookie(self.CODE_COOKIE_KEY, request_token)
        return response


class OAuthCallback(LoginRequiredMixin, ConsumerKeyMixin, View):
    OAUTH_AUTHORIZE_URL = "https://getpocket.com/v3/oauth/authorize"

    http_method_names = ["GET"]

    # TODO consider having a confirm login to pocket screen on GET instead
    def get(self, *args, **kwargs):
        state = self.request.COOKIES[self.STATE_COOKIE_KEY]
        # TODO do we get this back in the GET params instead
        code = self.request.CODE_COOKIE_KEY[self.CODE_COOKIE_KEY]
        pkt_resp = requests.post(self.OAUTH_AUTHORIZE_URL, json={"consumer_key": self.consumer_key, "code": code})
        pkt_body = pkt_resp.json()
        access_token = pkt_body["access_token"]
        print(access_token)
        print(state)
        # TODO delete cookies
        # TODO save access token to database
