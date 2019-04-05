import newspaper

from badfeed.feeds.models import Entry


class Enricher:
    def __init__(self, entry: Entry):
        self.entry = entry

    def enrich(self):
        html = self.extract_page_html()
        article = self.to_newspaper_article(html)
        self.save_to_entry(article)

    def save_to_entry(self, article: newspaper.Article):
        self.entry.content = article.text
        self.entry.save()

    def extract_page_html(self) -> str:
        raise NotImplementedError()

    def get_start_url(self) -> str:
        return self.entry.link

    def to_newspaper_article(self, html: str) -> newspaper.Article:
        article = newspaper.api.build_article()
        article.set_html(html)
        article.parse()
        return article
