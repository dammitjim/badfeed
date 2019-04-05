import requests

from badfeed.ingest.enricher.base import Enricher


class SimpleEnricher(Enricher):
    """No smart navigation, simply hit the URL directly and pass the raw HTML back."""

    def extract_page_html(self) -> str:
        url = self.get_start_url()
        response = requests.get(url)
        return response.text
