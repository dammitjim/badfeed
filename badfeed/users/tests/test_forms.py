import pytest

from badfeed.users.forms import RegistrationForm
from badfeed.users.models import BadFeedUser


@pytest.mark.django_db
class TestRegistrationForm:
    def test_valid_data(self, registration_form_data):
        """Should work with valid data."""
        form = RegistrationForm(registration_form_data)
        assert form.is_valid()

    @pytest.mark.parametrize("field", ["email", "confirm_email", "username", "password1", "password2"])
    def test_required_fields(self, field):
        """Test the appropriate fields are required."""
        form = RegistrationForm()
        assert form.fields[field].required

    def test_emails_must_match(self, registration_form_data):
        """The email fields must match."""
        registration_form_data["confirm_email"] = "butts@butts.com"
        form = RegistrationForm(data=registration_form_data)
        assert "confirm_email" in form.errors
        assert RegistrationForm.Errors.EMAIL_MISMATCH in form.errors["confirm_email"]

    def test_passwords_must_match(self, registration_form_data):
        """The passwords must match."""
        registration_form_data["password2"] = "badPassword!123"
        form = RegistrationForm(data=registration_form_data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_creates_user(self, registration_form_data):
        """Successful validation creates a user."""
        form = RegistrationForm(data=registration_form_data)
        form.save()
        assert BadFeedUser.objects.filter(
            username=registration_form_data["username"], email=registration_form_data["email"]
        ).exists()

    def test_email_taken(self, registration_form_data, user):
        """Emails already registered do not create users."""
        registration_form_data["email"] = user.email
        registration_form_data["confirm_email"] = user.email
        form = RegistrationForm(data=registration_form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_username_taken(self, registration_form_data, user):
        """Usernames already registered do not create users"""
        registration_form_data["username"] = user.username
        form = RegistrationForm(data=registration_form_data)
        assert not form.is_valid()
        assert "username" in form.errors
