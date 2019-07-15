from django.db import models

from feedzero.feeds.models import Feed


class IngestLog(models.Model):
    """Metric dumping ground until further notice.

    TODO this is somewhat inelegant, consider breaking out or
            tracking these metrics elsewhere
    """

    STATE_SUCCESS = "success"
    STATE_PARTIAL = "partial"
    STATE_FAILED = "failed"
    STATE_NOT_RESPONDING = "not_responding"
    STATE_CHOICES = [
        (STATE_SUCCESS, "Success"),
        (STATE_PARTIAL, "Partial"),
        (STATE_FAILED, "Failed"),
        (STATE_NOT_RESPONDING, "Not responding"),
    ]
    state = models.CharField(max_length=15, choices=STATE_CHOICES)
    body = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feed, related_name="ingest_logs", on_delete=models.CASCADE)

    def __str__(self):
        """Supply some debug information in string representation."""
        return f"{self.date_created} {self.feed.title} {self.state}"
