import pytest

from badfeed.feeds.models import EnrichedContent
from badfeed.ingest.enricher.base import Enricher


@pytest.mark.django_db
class TestEnricher:
    @pytest.fixture
    def enricher(self, entry):
        return Enricher(entry)

    def test_extract_page_html_raises_not_implemented(self, enricher):
        """Should raise a not implemented error in the base enricher."""
        with pytest.raises(NotImplementedError):
            enricher.extract_page_html()

    def test_get_start_url(self, enricher):
        """Should return the entry's link as the starting point."""
        assert enricher.get_start_url() == enricher.entry.link

    def test_save_uses_entry_summary_as_fallback(self, enricher, newspaper_article):
        """Should use summary as fallback if article summary is not available."""
        enricher.entry.summary = "This is only a test"
        newspaper_article.summary = None

        enricher.save_to_entry(newspaper_article)

        content = EnrichedContent.objects.get(entry=enricher.entry)
        assert content.summary == enricher.entry.summary

    def test_save_to_entry_creates_enriched_content(self, enricher, newspaper_article):
        """Should use all data available to create a new EnrichedContent object."""
        enricher.save_to_entry(newspaper_article)
        assert len(EnrichedContent.objects.filter(entry=enricher.entry)) == 1

    def test_save_to_entry_enriches_with_article_text(
        self, enricher, newspaper_article
    ):
        """Should load the article text into the enricher content."""
        enricher.save_to_entry(newspaper_article)
        content = EnrichedContent.objects.get(entry=enricher.entry)
        assert content.content == newspaper_article.text

    def test_save_to_entry_enriches_with_article_summary(
        self, enricher, newspaper_article
    ):
        """Should load the article summary into the enricher content."""
        enricher.save_to_entry(newspaper_article)
        content = EnrichedContent.objects.get(entry=enricher.entry)
        assert content.summary == newspaper_article.summary

    def test_enrich_doesnt_run_against_already_enriched(
        self, mocker, enricher, enriched_content_factory
    ):
        """Should not attempt to re-enrich enriched content."""
        enriched_content_factory(entry=enricher.entry)
        fn = mocker.patch("badfeed.ingest.enricher.base.Enricher.save_to_entry")
        enricher.enrich()
        fn.assert_not_called()

    def test_enrich_entry(self, mocker, enricher, newspaper_article):
        """Should take loaded article and enrich entry with it's data."""
        html_fn = mocker.patch(
            "badfeed.ingest.enricher.base.Enricher.extract_page_html"
        )
        html_fn.return_value = "html_to_parse"

        article_fn = mocker.patch(
            "badfeed.ingest.enricher.base.convert_html_to_newspaper"
        )
        article_fn.return_value = newspaper_article

        enricher.enrich()

        html_fn.assert_called()
        article_fn.assert_called_with("html_to_parse")
        assert len(EnrichedContent.objects.filter(entry=enricher.entry)) == 1
