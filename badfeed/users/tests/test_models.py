import pytest

from badfeed.users.models import BadFeedUser


@pytest.mark.django_db
class TestBadFeedUserModel:
    def test_email_field_unique(self):
        """The email field on the user model should be unique."""
        assert BadFeedUser._meta.get_field("email").unique

    def test_watching_field_blank(self):
        """The watching field should allow 0 entries."""
        assert BadFeedUser._meta.get_field("watching").blank

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
