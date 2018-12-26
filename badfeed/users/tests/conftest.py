import pytest


@pytest.fixture()
def registration_form_data():
    """Valid by default."""
    return {
        "username": "user1",
        "email": "user1@test.com",
        "confirm_email": "user1@test.com",
        "password1": "CoolPass!123",
        "password2": "CoolPass!123",
    }
