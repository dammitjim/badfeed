from django.db import models
from django.core.exceptions import FieldError
from slugify import slugify


class Slugified(models.Model):
    # TODO: much of this can be removed for UniqueSlugify in awesome-slugify
    SLUG_SOURCE_ATTR = "slugify_source"

    slug = models.SlugField(blank=True, max_length=200)

    def __init__(self, *args, **kwargs):
        """Check for presence of slugify_source."""
        super().__init__(*args, **kwargs)
        if not hasattr(self, self.SLUG_SOURCE_ATTR):
            raise FieldError(f"{self.__class__} requires {self.SLUG_SOURCE_ATTR} to use Slugified abstract class.")

    def save(self, *args, **kwargs):
        """Use the lookup result from self.slugify_source to load our slug."""
        if not self.slug:
            slug_attr = getattr(self, self.SLUG_SOURCE_ATTR)
            slug_source = getattr(self, slug_attr)
            self.slug = self.generate_slug(slug_source[:200])
        super().save(*args, **kwargs)

    def get_additional_slug_filters(self):
        return {}

    def generate_slug(self, slug_source, extra=0):
        """Generate slug from slug source defined on concrete class."""
        # TODO can replace this with unique slugify
        append = f"-{extra}" if extra > 0 else ""
        slug = slugify(slug_source, to_lower=True) + append
        while type(self).objects.filter(slug=slug, **self.get_additional_slug_filters()).exists():
            # OH BABY
            return self.generate_slug(slug_source, extra=extra + 1)
        return slug

    class Meta:
        abstract = True
