import pytest

from badfeed.users.forms import RegistrationForm
from badfeed.users.models import BadFeedUser


@pytest.mark.django_db
class TestRegistrationForm:
    @pytest.fixture()
    def form_data(self):
        """Valid by default."""
        return {
            "username": "user1",
            "email": "user1@test.com",
            "confirm_email": "user1@test.com",
            "password1": "CoolPass!123",
            "password2": "CoolPass!123",
        }

    def test_valid_data(self, form_data):
        """Should work with valid data."""
        form = RegistrationForm(form_data)
        assert form.is_valid()

    @pytest.mark.parametrize("field", ["email", "confirm_email", "username", "password1", "password2"])
    def test_required_fields(self, field):
        """Test the appropriate fields are required."""
        form = RegistrationForm()
        assert form.fields[field].required

    def test_emails_must_match(self, form_data):
        """The email fields must match."""
        form_data["confirm_email"] = "butts@butts.com"
        form = RegistrationForm(data=form_data)
        assert "confirm_email" in form.errors
        assert RegistrationForm.Errors.EMAIL_MISMATCH in form.errors["confirm_email"]

    def test_passwords_must_match(self, form_data):
        """The passwords must match."""
        form_data["password2"] = "badPassword!123"
        form = RegistrationForm(data=form_data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_creates_user(self, form_data):
        """Successful validation creates a user."""
        form = RegistrationForm(data=form_data)
        form.save()
        assert BadFeedUser.objects.filter(username=form_data["username"], email=form_data["email"]).exists()

    def test_email_taken(self, form_data, user):
        """Emails already registered do not create users."""
        form_data["email"] = user.email
        form_data["confirm_email"] = user.email
        form = RegistrationForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_username_taken(self, form_data, user):
        """Usernames already registered do not create users"""
        form_data["username"] = user.username
        form = RegistrationForm(data=form_data)
        assert not form.is_valid()
        assert "username" in form.errors
