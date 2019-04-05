from selenium.webdriver.remote.webdriver import WebDriver

from badfeed.ingest.enricher.base import Enricher


class SeleniumEnricher(Enricher):
    """Enrich a database entry with content that is closer to the source by parsing the webpage.

    Likely to provide mixed results, especially as we're navigating the minefield of selenium
    but it may help for the feeds which just provide a snippet and a "read more" link to drive
    traffic.

    # TODO needs a lot of work
    """

    # TODO add user agent that is consistent with everything else
    BROWSER_CAPABILITIES = {"browserName": "chrome", "javascriptEnabled": True}

    def __init__(self, *args, driver: WebDriver = None, **kwargs):
        """Load entry and optional selenium webdriver into class."""
        super().__init__(*args, **kwargs)
        self.driver = driver
        if not self.driver:
            self.driver = WebDriver(desired_capabilities=self.BROWSER_CAPABILITIES)

    def extract_page_html(self) -> str:
        self.driver.get(self.get_start_url())
        if self._smells_like_a_consent_page():
            self._get_submit_button().click()
        return self.driver.page_source

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

    # TODO this could, with a lot more thought, be a part of the base class
    #   might need some classification of pages here, look into that.
    def _smells_like_a_consent_page(self):
        source = self.driver.page_source
        return any([beef in source for beef in self.CONSENT_PAGE_BEEF])

    def _get_submit_button(self):
        return self.driver.find_element_by_xpath("//input[@type='submit']")
