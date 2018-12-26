from django import forms
from django.contrib.auth.forms import UserCreationForm

from badfeed.users.models import BadFeedUser


class RegistrationForm(UserCreationForm):
    confirm_email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_widgets()

    def _load_widgets(self):
        """Loads in some bootstrap attributes for the form elements."""
        self.fields["confirm_email"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm email"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm password"})
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        model = BadFeedUser

    def clean_confirm_email(self):
        """Ensure the email fields match."""
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(self.Errors.EMAIL_MISMATCH)
        return confirm_email

    class Errors:
        EMAIL_MISMATCH = "The two email fields didn't match."
