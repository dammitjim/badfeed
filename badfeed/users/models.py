from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models

from badfeed.feeds.models import Feed


class BadFeedUser(AbstractUser):

    email = models.EmailField(unique=True)
    watching = models.ManyToManyField(Feed, related_name="watched_by", blank=True)

    def _store_third_party_token(self, provider, code):
        filter_kwargs = {"provider": provider, "user": self}
        if ThirdPartyTokens.objects.filter(**filter_kwargs).exists():
            ThirdPartyTokens.objects.get(**filter_kwargs).delete()
        return ThirdPartyTokens.objects.create(code=code, **filter_kwargs)

    def store_pocket_token(self, code):
        """Assign a new pocket token to the user."""
        return self._store_third_party_token(ThirdPartyTokens.PROVIDER_POCKET, code)

    def watch(self, feed, commit=False):
        """Watch feed if possible."""
        if self.watching.filter(pk=feed.pk).exists():
            raise ValueError("You are already watching this feed.")

        self.watching.add(feed)
        if commit:
            self.save()

    def unwatch(self, feed, commit=False):
        """Unwatch feed if possible."""
        if not self.watching.filter(pk=feed.pk).exists():
            raise ValueError("You are not watching this feed")

        self.watching.remove(feed)
        if commit:
            self.save()


class ThirdPartyTokens(models.Model):
    PROVIDER_POCKET = "pocket"
    PROVIDER_CHOICES = [(PROVIDER_POCKET, "Pocket")]

    code = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    metadata = JSONField(blank=True, null=True)
    user = models.ForeignKey(BadFeedUser, related_name="third_party_tokens", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("provider", "user"),)
