from django.conf import settings
from django.contrib.auth import get_user
from django.test import override_settings, RequestFactory
from django.urls import reverse
import pytest

from badfeed.users.integrations.pocket.views import (
    PocketConsumerKeyMixin,
    OAuthCallback,
    OAuthEntry,
)
from badfeed.users.models import ThirdPartyTokens


@pytest.mark.django_db
class TestOAuthEntry:
    def setup(self):
        """Load non-instance parameters into class."""
        self.url = reverse("users:pocket:oauth_entry")

    def test_sets_state_cookie(self, mocker, auth_client):
        """The view should set a state cookie in the response."""
        token_fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token"
        )
        token_fn.return_value = "123"
        auth_fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url"
        )
        auth_fn.return_value = "/my-cool-redirect"
        uuid_fn = mocker.patch("badfeed.users.integrations.pocket.views.uuid4")
        uuid_fn.return_value = "456"

        auth_client.get(self.url)
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.STATE_COOKIE_KEY).value
            == "456"
        )

    def test_sets_code_cookie_to_pocket_value(self, mocker, auth_client):
        """The view should set the code cookie to the pocket token."""
        token_fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token"
        )
        token_fn.return_value = "123"
        auth_fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url"
        )
        auth_fn.return_value = "/my-cool-redirect"

        auth_client.get(self.url)
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.CODE_COOKIE_KEY).value
            == "123"
        )

    def test_redirects_to_pocket(self, mocker, auth_client):
        """Should redirect to the value provided by pocket auth."""
        mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token"
        )
        auth_fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url"
        )
        auth_fn.return_value = "/my-cool-redirect"

        response = auth_client.get(self.url)
        assert response.status_code == 302
        assert response.url == "/my-cool-redirect"

    def test_get_redirect_url_produces_absolute_url(self):
        """The function should return an absolute URL.

        This is important as it gets passed to pocket as a GET
        query parameter.
        """
        request = RequestFactory().get(self.url)
        view = OAuthEntry()
        view.request = request

        callback_url = reverse("users:pocket:oauth_callback")
        assert view._get_redirect_url() == f"http://testserver{callback_url}"

    def test_login_required(self, client):
        """The view should only be available to logged in users."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    @override_settings(POCKET_CONSUMER_KEY="definitely-a-thing")
    def test_uses_consumer_key_from_settings(self):
        """The view should load the pocket consumer key from settings."""
        view = OAuthEntry()
        assert view.consumer_key == "definitely-a-thing"


@pytest.mark.django_db
class TestOAuthCallback:
    def setup(self):
        """Load non-instance variables into class."""
        self.url = reverse("users:pocket:oauth_callback")

    def test_login_required(self, client):
        """The view should only be available to logged in users."""
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == f"{settings.LOGIN_URL}?next={self.url}"

    def test_deletes_state_cookie(self, mocker, auth_client):
        """Once we have done the callback, delete the state cookie."""
        mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthCallback._set_access_token_to_user"
        )
        auth_client.cookies[PocketConsumerKeyMixin.STATE_COOKIE_KEY] = "123"
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.STATE_COOKIE_KEY).value
            == "123"
        )
        auth_client.get(self.url)
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.STATE_COOKIE_KEY).value == ""
        )

    def test_deletes_code_cookie(self, mocker, auth_client):
        """Once we have done the callback, delete the code cookie."""
        mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthCallback._set_access_token_to_user"
        )
        auth_client.cookies[PocketConsumerKeyMixin.CODE_COOKIE_KEY] = "123"
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.CODE_COOKIE_KEY).value
            == "123"
        )
        auth_client.get(self.url)
        assert (
            auth_client.cookies.get(PocketConsumerKeyMixin.CODE_COOKIE_KEY).value == ""
        )

    def test_loads_code_from_cookie(self, mocker, auth_client):
        """We should be sending the code from the cookie to pocket."""
        fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthCallback._get_access_token"
        )
        fn.return_value = "456"
        auth_client.cookies[PocketConsumerKeyMixin.CODE_COOKIE_KEY] = "123"
        auth_client.get(self.url)
        fn.assert_called_with("123")

    def test_creates_access_token_object(self, mocker, auth_client):
        """On all success, create a ThirdPartyToken object on the user."""
        fn = mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthCallback._get_access_token"
        )
        fn.return_value = "456"
        auth_client.cookies[PocketConsumerKeyMixin.CODE_COOKIE_KEY] = "123"
        auth_client.get(self.url)
        assert ThirdPartyTokens.objects.filter(
            user=get_user(auth_client),
            provider=ThirdPartyTokens.PROVIDER_POCKET,
            code="456",
        ).exists()

    def test_redirects_to_success_url(self, mocker, auth_client):
        """On success, redirect to the given success url property."""
        mocker.patch(
            "badfeed.users.integrations.pocket.views.OAuthCallback._set_access_token_to_user"
        )
        response = auth_client.get(self.url)
        assert response.status_code == 302
        assert response.url == OAuthCallback.success_url
