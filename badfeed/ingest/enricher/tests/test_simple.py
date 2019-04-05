import pytest

from badfeed.ingest.constants import REQUESTS_USER_AGENT
from badfeed.ingest.enricher.simple import SimpleEnricher


@pytest.mark.django_db
class TestSimpleEnricher:
    @pytest.fixture
    def enricher(self, entry):
        return SimpleEnricher(entry)

    def test_sends_correct_user_agent(self, mocker, enricher):
        """Should send the feedzero user agent."""
        req_fn = mocker.patch("badfeed.ingest.enricher.simple.requests.get")
        req_mock = mocker.Mock()
        req_mock.status_code = 200
        req_fn.return_value = req_mock

        enricher.extract_page_html()
        req_fn.assert_called_with(
            enricher.entry.link, headers={"User-Agent": REQUESTS_USER_AGENT}
        )

    def test_returns_response_text(self, mocker, enricher):
        """Should return the raw response text."""
        req_fn = mocker.patch("badfeed.ingest.enricher.simple.requests.get")
        req_mock = mocker.Mock()
        req_mock.status_code = 200
        req_mock.text = "This is only a test"
        req_fn.return_value = req_mock

        html = enricher.extract_page_html()
        assert html == "This is only a test"

    def test_invalid_status_code_raises(self, mocker, enricher):
        """Should raise if a non 200 status code is received."""
        req_fn = mocker.patch("badfeed.ingest.enricher.simple.requests.get")
        req_mock = mocker.Mock()
        req_mock.status_code = 400
        req_fn.return_value = req_mock

        with pytest.raises(ValueError):
            enricher.extract_page_html()
