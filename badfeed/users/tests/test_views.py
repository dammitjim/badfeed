from django.contrib.messages import get_messages
from django.urls import reverse
import pytest

from badfeed.users import views


@pytest.mark.django_db
class TestLoginView:
    def setup(self):
        self.url = reverse("users:login")

    def test_logged_in_users_redirect(self, auth_client):
        """Logged in users should not be able to log in again."""
        response = auth_client.get(self.url)
        assert response.status_code == 302
        str_msg = [
            m.message for m in get_messages(response.wsgi_request)._queued_messages
        ]
        assert views.LoginView.Messages.ALREADY_LOGGED_IN in str_msg

    def test_renders(self, client):
        """The login view should render."""
        response = client.get(self.url)
        assert response.status_code == 200
