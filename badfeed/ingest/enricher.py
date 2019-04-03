import newspaper
from selenium.webdriver.remote.webdriver import WebDriver

from badfeed.feeds.models import Entry


class EntryContentEnricher:
    """Enrich a database entry with content that is closer to the source by parsing the webpage.

    Likely to provide mixed results, especially as we're navigating the minefield of selenium
    but it may help for the feeds which just provide a snippet and a "read more" link to drive
    traffic.
    """

    BROWSER_CAPABILITIES = {"browserName": "chrome", "javascriptEnabled": True}

    def __init__(self, entry: Entry, driver: WebDriver = None):
        """Load entry and optional selenium webdriver into class."""
        self.entry = entry
        self.driver = driver
        if not self.driver:
            self.driver = WebDriver(desired_capabilities=self.BROWSER_CAPABILITIES)

    def enrich(self):
        """Take the loaded database entry and enrich the content with the parsed text."""
        self.driver.get(self.entry.url)
        if self._smells_like_a_consent_page():
            self._get_submit_button().click()

        article = self._get_newspaper_article()
        self.entry.content = article.text
        self.entry.save()

    CONSENT_PAGE_BEEF = [
        "relevant ads",
        "collect data",
        "use data",
        "our partners",
        "GDPR",
        "consent",
        "set cookies",
        "use your data",
    ]

    def _smells_like_a_consent_page(self):
        source = self.driver.page_source
        return any([beef in source for beef in self.CONSENT_PAGE_BEEF])

    def _get_submit_button(self):
        return self.driver.find_element_by_xpath("//input[@type='submit']")

    def _get_newspaper_article(self):
        article = newspaper.api.build_article()
        article.set_html(self.driver.page_source)
        article.parse()
        return article
