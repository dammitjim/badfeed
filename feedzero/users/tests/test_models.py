from django.db.utils import IntegrityError
import pytest

from feedzero.users.models import feedzeroUser, ThirdPartyTokens


@pytest.mark.django_db
class TestfeedzeroUserModel:
    def test_email_field_unique(self):
        """The email field on the user model should be unique."""
        assert feedzeroUser._meta.get_field("email").unique

    def test_watching_field_blank(self):
        """The watching field should allow 0 entries."""
        assert feedzeroUser._meta.get_field("watching").blank

    def test_dunder_str(self, user):
        """The model should return the username as the string value."""
        assert str(user) == "BadUser"

    def test_watch_new_feed(self, user, feed):
        """The watch method should allow a user to follow a new feed."""
        user.watch(feed, commit=True)
        assert user.watching.filter(pk=feed.pk).exists()

    def test_watch_existing_feed_raises(self, user, feed):
        """The watch method should raise if the user is already watching the feed."""
        user.watch(feed, commit=True)
        with pytest.raises(ValueError):
            user.watch(feed, commit=True)

    def test_store_pocket_token_creates_object(self, user):
        """The method should create a new ThirdPartyToken object."""
        assert not ThirdPartyTokens.objects.filter(
            user=user, provider=ThirdPartyTokens.PROVIDER_POCKET
        ).exists()
        user.store_pocket_token("123")
        assert ThirdPartyTokens.objects.filter(
            user=user, provider=ThirdPartyTokens.PROVIDER_POCKET
        ).exists()

    def test_store_pocket_token_replaces_existing_token(self, user):
        """If a token already exists for this provider, replace it."""
        user.store_pocket_token("123")
        user.store_pocket_token("456")
        assert (
            ThirdPartyTokens.objects.get(
                user=user, provider=ThirdPartyTokens.PROVIDER_POCKET
            ).code
            == "456"
        )


@pytest.mark.django_db
class TestThirdPartyTokensModel:
    def setup(self):
        """Load some non-instance test data."""
        self.model = ThirdPartyTokens

    def test_code_required(self):
        """The code field should be required."""
        assert not self.model._meta.get_field("code").blank
        assert not self.model._meta.get_field("code").null

    def test_provider_required(self):
        """The provider field should be required."""
        assert not self.model._meta.get_field("provider").blank
        assert not self.model._meta.get_field("provider").null

    def test_provider_user_are_unique_together(self, third_party_token_factory):
        """The user cannot have more than 1 token per provider."""
        token = third_party_token_factory()
        with pytest.raises(IntegrityError):
            third_party_token_factory(user=token.user, provider=token.provider)
