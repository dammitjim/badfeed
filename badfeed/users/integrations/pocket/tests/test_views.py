import pytest
from django.conf import settings
from django.test import RequestFactory, override_settings
from django.urls import reverse

from badfeed.users.integrations.pocket.views import ConsumerKeyMixin, OAuthEntry


@pytest.mark.django_db
class TestOAuthEntry:
    def setup(self):
        """Load non-instance parameters into class."""
        self.url = reverse("users:pocket:oauth_entry")

    def test_sets_state_cookie(self, mocker, auth_client):
        """The view should set a state cookie in the response."""
        token_fn = mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token")
        token_fn.return_value = "123"
        auth_fn = mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url")
        auth_fn.return_value = "/my-cool-redirect"
        uuid_fn = mocker.patch("badfeed.users.integrations.pocket.views.uuid4")
        uuid_fn.return_value = "456"

        auth_client.get(self.url)
        assert auth_client.cookies.get(ConsumerKeyMixin.STATE_COOKIE_KEY).value == "456"

    def test_sets_code_cookie_to_pocket_value(self, mocker, auth_client):
        """The view should set the code cookie to the pocket token."""
        token_fn = mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token")
        token_fn.return_value = "123"
        auth_fn = mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url")
        auth_fn.return_value = "/my-cool-redirect"

        auth_client.get(self.url)
        assert auth_client.cookies.get(ConsumerKeyMixin.CODE_COOKIE_KEY).value == "123"

    def test_redirects_to_pocket(self, mocker, auth_client):
        """Should redirect to the value provided by pocket auth."""
        mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_request_token")
        auth_fn = mocker.patch("badfeed.users.integrations.pocket.views.OAuthEntry._get_auth_url")
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
