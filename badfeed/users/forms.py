from django import forms
from django.contrib.auth.forms import UserCreationForm

from badfeed.users.models import BadFeedUser


class RegistrationForm(UserCreationForm):
    confirm_email = forms.EmailField(required=True)

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
