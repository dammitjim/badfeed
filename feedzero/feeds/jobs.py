import tempfile
from urllib.parse import urlparse

from django.core import files
from django_rq import job
import favicon
import requests

from feedzero.ingest.constants import REQUESTS_USER_AGENT


@job
def enrich_feed_with_favicon(feed):
    """Pull down favicon from available URL.

    TODO if any part of this fails, need a placeholder image.
    """
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
    filename = f"{feed.slug}.{icon.format}"
    lf = tempfile.NamedTemporaryFile()
    for chunk in response.iter_content(1024):
        lf.write(chunk)
    feed.logo.save(filename, files.File(lf))
