"""TODO this file needs filling out with substantially more tests."""
import maya
import pytest

from badfeed.ingest.exceptions import ContentErrorException
from badfeed.ingest.parser import EntryParser, RSSParser


class TestEntryParser:
    @pytest.fixture
    def valid_data(self, valid_data_partial):
        valid_data_partial.content = "Test content"
        valid_data_partial.summary_detail = "Test summary detail"
        return valid_data_partial

    @pytest.fixture
    def valid_data_partial(self, mocker):
        m = mocker.Mock()
        m.title = "This is only a test"
        m.link = "https://tightenupthe.tech"
        m.id = "testguid"
        m.published = str(maya.now())
        m.content = None
        m.summary_detail = None
        m.description = None
        m.summary = None
        return m

    def test_init_loads_entry_data(self, mocker):
        """Should load the supplied entry data into the class on init."""
        mocked_data = mocker.MagicMock()
        parser = EntryParser(mocked_data)
        assert parser.entry_data == mocked_data

    def test_load_replaces_entry_data(self, mocker):
        """Should replace existing entry_data on call to load."""
        mocked_data_foo = mocker.MagicMock()
        mocked_data_bar = mocker.MagicMock()
        parser = EntryParser(mocked_data_foo)
        parser.load(mocked_data_bar)
        assert parser.entry_data == mocked_data_bar

    def test_extracts_title(self, valid_data):
        """Should extract the title from the loaded entry_data."""
        parser = EntryParser(valid_data)
        data = parser.extract()
        assert data["title"] == "This is only a test"

    def test_extracts_link(self, valid_data):
        """Should extract the link from the loaded entry_data."""
        parser = EntryParser(valid_data)
        data = parser.extract()
        assert data["link"] == "https://tightenupthe.tech"

    def test_extracts_guid(self, valid_data):
        """Should extract the guid from the loaded entry_data."""
        parser = EntryParser(valid_data)
        data = parser.extract()
        assert data["guid"] == "testguid"

    def test_extracts_content_from_content_field(self, valid_data):
        """Should extract content from content field (over description)."""
        parser = EntryParser(valid_data)
        data = parser.extract()
        assert data["content"] == "Test content"

    def test_extracts_content_from_fallback_description(self, valid_data_partial):
        """Should use description if no content available."""
        valid_data_partial.description = "Test description"
        valid_data_partial.summary = "Test summary"
        parser = EntryParser(valid_data_partial)
        data = parser.extract()
        assert data["content"] == "Test description"

    def test_raises_if_no_content_field_found(self, valid_data_partial):
        """Should raise if no appropriate content field is present."""
        with pytest.raises(ContentErrorException):
            parser = EntryParser(valid_data_partial)
            parser.extract()

    def test_extracts_summary_from_summary_detail(self, valid_data):
        """Should extract summary from summary detail if present."""
        parser = EntryParser(valid_data)
        data = parser.extract()
        assert data["summary"] == "Test summary detail"

    def test_extracts_summary_from_summary_fallback(self, valid_data_partial):
        """Should extract summary from summary as fallback."""
        valid_data_partial.description = "Test description"
        valid_data_partial.summary = "Test summary"
        parser = EntryParser(valid_data_partial)
        data = parser.extract()
        assert data["summary"] == "Test summary"

    def test_raises_if_no_summary_field_found(self, valid_data_partial):
        """Should raise if no appropriate summary field is present."""
        valid_data_partial.description = "Test description"
        with pytest.raises(ContentErrorException):
            parser = EntryParser(valid_data_partial)
            parser.extract()

    # TODO parametrize
    def test_extract_cleans_content(self):
        """Should clean out any schmuck from the content field."""
        pass

    # TODO parametrize
    def test_date_published_parsing(self):
        """Should handle various date published strings."""
        pass

    # TODO parametrize
    def test_extract_cleans_summary(self):
        """Should clean out any schmuck from the content field."""
        pass


@pytest.mark.django_db
class TestRSSParser:
    def test_initialises_with_feed(self, feed):
        """Should load the feed into the class on init."""
        parser = RSSParser(feed)
        assert parser.FEED == feed

    def test_omits_existing_entries(self, mocker, entry):
        """Should omit any entries with a corresponding database entry for the feed."""
        mocked_entry_1 = mocker.MagicMock()
        mocked_entry_1.id = entry.pk + 1

        mocked_entry_2 = mocker.MagicMock()
        mocked_entry_2.id = entry.guid

        entries = [mocked_entry_1, mocked_entry_2]

        parser = RSSParser(feed=entry.feed)
        assert list(parser.get_entries_to_process(entries)) == [mocked_entry_1]

    def test_allows_duplicate_guid_across_different_feeds(
        self, mocker, feed_factory, entry_factory
    ):
        """Should allow the same guid through as long as the feed is different."""
        feed_1 = feed_factory()
        entry_1 = entry_factory(feed=feed_1)

        # mock an entry with the same guid, but a different feed
        mocked_entry_1 = mocker.MagicMock()
        mocked_entry_1.id = entry_1.guid

        parser = RSSParser(feed=feed_factory())
        assert list(parser.get_entries_to_process([mocked_entry_1])) == [mocked_entry_1]

    def test_creates_database_entry(self):
        """Should create database entry if valid data."""
        pass

    def test_attaches_tags_if_extracted(self):
        """Should attach tags to entry if they are extracted from the data."""
        pass

    def test_attaches_entry_to_initialised_feed(self):
        """Should save any entries to the database attached to the initialised feed."""
        pass

    def test_logs_failed_cleans(self):
        """Should log an exception if an entry fails to clean."""
        pass

    def test_exception_creates_response_log(self):
        """Should create a response log if any exception happens.

        This is so we can identify problematic formatting and use the files for regression
        tests should any bugs arise.
        """
        pass
