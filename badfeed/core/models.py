from django.db import models
from slugify import UniqueSlugify


class SlugifiedMixin(models.Model):
    slug = models.SlugField(blank=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            checker = UniqueSlugify(unique_check=self.slug_uniqueness_check, to_lower=True, max_length=200)
            self.slug = checker(self.get_slug_attr(), uids=self.get_initial_slug_uids())
        return super().save(*args, **kwargs)

    def get_slug_attr(self):
        return self.title

    def get_initial_slug_uids(self):
        return []

    @staticmethod
    def slug_uniqueness_check(text, uids):
        return text not in uids

    class Meta:
        abstract = True
