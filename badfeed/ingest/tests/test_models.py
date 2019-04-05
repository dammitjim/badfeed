import pytest

from badfeed.ingest.models import IngestLog


@pytest.mark.django_db
class TestIngestLog:
    @pytest.mark.parametrize("state", [state[0] for state in IngestLog.STATE_CHOICES])
    def test_can_create_different_log_states(self, feed, state):
        """Should be able to create each potential state."""
        log = IngestLog.objects.create(state=state, feed=feed)
        assert log.state == state

    def test_feed_deletion_cascades(self, feed, ingest_log_factory):
        """Should delete corresponding logs if the related feed is deleted."""
        log1 = ingest_log_factory(feed=feed)
        log2 = ingest_log_factory(feed=feed)
        feed.delete()
        assert len(IngestLog.objects.filter(pk__in=[log1.pk, log2.pk])) == 0
