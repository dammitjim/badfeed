from urllib.parse import urlparse

from django_rq import job
import favicon
import requests

from feedzero.feeds.models import Feed
from feedzero.ingest.constants import REQUESTS_USER_AGENT


@job
def enrich_feed_with_favicon(feed: Feed):
    """Pull down favicon from available URL."""
    uri = urlparse(feed.link)
    link = f"{uri.scheme}://{uri.netloc}"

    icons = []
    if link:
        icons = favicon.get(link, headers={"User-Agent": REQUESTS_USER_AGENT})
    if len(icons) == 0:
        # TODO log unable to get favicon?
        return

    icon = icons[0]
    response = requests.get(icon.url, stream=True)
    with open(f"/tmp/{feed.slug}.{icon.format}", "wb") as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)
