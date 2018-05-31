from django.db import models

from badfeed.core.models import Slugified


class Feed(Slugified, models.Model):
    """A feed of content."""

    slugify_source = "title"

    title = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_last_scraped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    """An author of an entry."""

    name = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="authors")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """A tag to categories entries."""

    term = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=1000, blank=True, null=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.term


class Entry(Slugified, models.Model):
    """An entry into a Feed."""

    slugify_source = "title"

    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    guid = models.CharField(max_length=1000)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)

    date_published = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="entries")

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, related_name="entries")
    contributors = models.ManyToManyField(Author, related_name="contributed_to")

    tags = models.ManyToManyField(Tag, related_name="entries")

    def get_additional_slug_filters(self):
        """Used by Slugified to help generate the slug by uniqueness."""
        return {"feed": self.feed}

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "entries"
        unique_together = (("guid", "feed"),)


class Enclosure(models.Model):
    """A media file."""

    href = models.CharField(max_length=1000)
    file_type = models.CharField(max_length=1000)
    # TODO this seems dirty but I'm not sure of the best way to handle this
    length = models.TextField()

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return self.href
