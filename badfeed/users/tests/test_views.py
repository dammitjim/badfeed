from django.contrib.auth import get_user
from django.contrib.messages import get_messages
from django.urls import reverse
import pytest

from badfeed.users import views
from badfeed.users.models import BadFeedUser


@pytest.mark.django_db
class TestRegisterView:
    def setup(self):
        self.url = reverse("users:register")

    def test_logged_in_redirects(self, auth_client):
        """If a user is already logged in, redirect them."""
        response = auth_client.get(self.url)
        messages = get_messages(response.wsgi_request)
        assert response.status_code == 302
        str_msg = [m.message for m in messages._queued_messages]
        assert views.RegisterView.Messages.ALREADY_REGISTERED in str_msg

    def test_renders(self, client):
        """The view should render."""
        response = client.get(self.url)
        assert response.status_code == 200

    def test_form_valid_creates_user(self, client, registration_form_data):
        """On successful submission, the user should be created."""
        assert len(BadFeedUser.objects.all()) == 0
        response = client.post(self.url, registration_form_data)
        assert response.status_code == 302
        assert len(BadFeedUser.objects.all()) == 1

    def test_form_valid_logs_in(self, client, registration_form_data):
        """On successful submission, should be logged in."""
        client.post(self.url, registration_form_data)
        user = get_user(client)
        assert user.is_authenticated
        assert user.username == registration_form_data["username"]

    def test_invalid_form_doesnt_create_user(self, client):
        """If the form is invalid, nothing should be created."""
        assert len(BadFeedUser.objects.all()) == 0
        response = client.post(self.url, {})
        assert response.status_code == 200
        assert len(BadFeedUser.objects.all()) == 0


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

    def test_valid_form_logs_user_in(self, client, user):
        """The view should log the user in."""
        new_pass = "Password123"
        user.set_password(new_pass)
        user.save()

        client.post(self.url, {"username": user.username, "password": new_pass})

        client_user = get_user(client)
        assert client_user.is_authenticated
        assert client_user == user

    def test_invalid_form_fails(self, client, user):
        """The view should log the user in."""
        new_pass = "Password123"
        user.set_password(new_pass)
        user.save()

        client.post(self.url, {"username": user.username, "password": "NotMyPassword"})

        client_user = get_user(client)
        assert not client_user.is_authenticated


@pytest.mark.django_db
class TestLogoutView:
    def setup(self):
        self.url = reverse("users:logout")

    def test_logs_user_out(self, auth_client):
        """The view should log out the user."""
        client_user = get_user(auth_client)
        assert client_user.is_authenticated
        auth_client.get(self.url)
        client_user = get_user(auth_client)
        assert not client_user.is_authenticated

    def test_redirects_after_logout(self, auth_client):
        """Should redirect to a non-default page on logout."""
        response = auth_client.get(self.url)
        assert response.status_code == 302
        assert response.url == "/"
