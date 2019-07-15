import requests

from feedzero.ingest.constants import REQUESTS_USER_AGENT
from feedzero.ingest.enricher.base import Enricher


class SimpleEnricher(Enricher):
    """No smart navigation, simply hit the URL directly and pass the raw HTML back."""

    def extract_page_html(self) -> str:
        url = self.get_start_url()
        response = requests.get(url, headers={"User-Agent": REQUESTS_USER_AGENT})
        if response.status_code != 200:
            raise ValueError(
                f"Enrichment request for url {url} failed with status code {response.status_code}"
            )
        return response.text
