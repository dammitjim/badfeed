from model_mommy import mommy
import pytest

from badfeed.ingest.models import IngestLog


@pytest.fixture
def ingest_log(feed):
    return mommy.make(IngestLog, feed=feed)


@pytest.fixture
def ingest_log_factory():
    def _make(feed, **kwargs):
        return mommy.make(IngestLog, feed=feed, **kwargs)

    return _make
