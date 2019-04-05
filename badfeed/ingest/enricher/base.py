import newspaper

from badfeed.feeds.models import Entry
from badfeed.ingest.enricher.utils import convert_html_to_newspaper


class Enricher:
    def __init__(self, entry: Entry):
        self.entry = entry

    def enrich(self):
        html = self.extract_page_html()
        article = convert_html_to_newspaper(html)
        self.save_to_entry(article)

    def save_to_entry(self, article: newspaper.Article):
        self.entry.content = article.text
        self.entry.save()

    def extract_page_html(self) -> str:
        raise NotImplementedError()

    def get_start_url(self) -> str:
        return self.entry.link
