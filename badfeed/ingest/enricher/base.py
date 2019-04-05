from loguru import logger
import newspaper

from badfeed.feeds.models import EnrichedContent, Entry
from badfeed.ingest.enricher.utils import convert_html_to_newspaper, get_sorted_images


class Enricher:
    def __init__(self, entry: Entry):
        self.entry = entry

    def enrich(self):
        if hasattr(self.entry, "enriched"):
            logger.warning(
                f"Attempting to enrich entry which already has enriched content: {self.entry.pk}"
            )
            return
        html = self.extract_page_html()
        article = convert_html_to_newspaper(html)
        self.save_to_entry(article)

    def save_to_entry(self, article: newspaper.Article):
        images = get_sorted_images(article)

        summary = article.summary
        if not summary:
            summary = self.entry.summary

        EnrichedContent(
            entry=self.entry,
            summary=summary,
            images=images,
            content=article.text,
            movies=article.movies,
        ).save()

    def extract_page_html(self) -> str:
        raise NotImplementedError()

    def get_start_url(self) -> str:
        return self.entry.link
