from django.db import models

from badfeed.feeds.models import Feed


class IngestLog(models.Model):
    """Metric dumping ground until further notice."""

    STATE_SUCCESS = "success"
    STATE_PARTIAL = "partial"
    STATE_FAILED = "failed"
    STATE_CHOICES = [
        (STATE_SUCCESS, "Success"),
        (STATE_PARTIAL, "Partial"),
        (STATE_FAILED, "Failed"),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    failing_xml = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feed, related_name="ingest_logs", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_created} {self.feed.title} {self.state}"
