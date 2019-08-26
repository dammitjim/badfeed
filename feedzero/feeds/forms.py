from django import forms
from django.conf import settings
import feedparser
import requests

from feedzero.feeds.jobs import enrich_feed_with_favicon
from feedzero.feeds.models import Feed
from feedzero.ingest.constants import REQUESTS_USER_AGENT


class FeedAddForm(forms.Form):
    url = forms.CharField(max_length=255, required=True)

    def clean_url(self):
        url = self.cleaned_data["url"]
        if Feed.objects.filter(link=url).exists():
            raise forms.ValidationError("Feed already exists with that URL.")

        response = requests.get(url, headers={"User-Agent": REQUESTS_USER_AGENT})
        if response.status_code != 200:
            raise forms.ValidationError(
                f"URL responded with status code {response.status_code}"
            )
        parse = feedparser.parse(response.text)
        if parse.bozo:
            raise forms.ValidationError(f"URL did not return parse-able data.")
        self.parse = parse
        self.url = url

    def insert(self):
        """Insert new Feed row from parsed data."""
        if not self.is_valid():
            raise forms.ValidationError("Cannot insert until form validated.")
        feed = Feed.objects.create(title=self.parse.feed.title, link=self.url)
        if settings.RQ_ENABLED:
            enrich_feed_with_favicon.delay(feed)
        else:
            enrich_feed_with_favicon(feed)
