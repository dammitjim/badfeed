from django.db import models
from slugify import UniqueSlugify


class SlugifiedMixin(models.Model):
    """Adds a slug field to the subclassed model."""

    slug = models.SlugField(blank=True, max_length=200)

    def save(self, *args, **kwargs):
        """Override save method to populate slug field on class."""
        # TODO change slug if title changes?
        if not self.slug:
            checker = UniqueSlugify(
                unique_check=self.slug_uniqueness_check, to_lower=True, max_length=200
            )
            self.slug = checker(self.get_slug_attr(), uids=self.get_initial_slug_uids())
        return super().save(*args, **kwargs)

    def get_slug_attr(self):
        """Get the attribute to use as the base for the slug.

        Defaults to title as that is most commonly used in the codebase.
        """
        return self.title

    def get_initial_slug_uids(self):
        """Populate a list of unique values for the slugify function to start from."""
        return []

    @staticmethod
    def slug_uniqueness_check(text, uids):
        """Default uniqueness check."""
        return text not in uids

    class Meta:
        abstract = True
