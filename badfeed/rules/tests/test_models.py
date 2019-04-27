from django.contrib.contenttypes.models import ContentType
import maya
import pytest


from badfeed.feeds.models import EntryState
from badfeed.rules.models import Rule


@pytest.mark.django_db
class TestRule:
    def test_assigns_rule_content_type_on_save(self, rule):
        """Should assign the base rule type to the content type field on save."""
        assert rule.content_type == ContentType.objects.get_for_model(Rule)

    def test_specific_returns_concrete_subclass(self, rule):
        """Should return the Rule subclass in the case of the underlying Rule class."""
        assert rule.specific == rule

    def test_apply_deleted(self, mocker, entry, rule_factory):
        """Should mark the corresponding entry as deleted."""
        rule = rule_factory(action=EntryState.STATE_DELETED)
        mocked_fn = mocker.patch("badfeed.feeds.models.Entry.mark_deleted")
        rule.apply(entry)
        mocked_fn.assert_called_with(rule.user)

    def test_apply_hidden(self):
        """Should mark the corresponding entry as hidden."""
        # TODO implement
        pass

    def test_manager_active_returns_valid_rules(self, rule_factory):
        """Should return rules which fall in a valid date range."""
        valid_rule = rule_factory(
            date_start=maya.now().subtract(days=2).datetime(),
            date_end=maya.now().add(days=5).datetime(),
        )
        active_rules = Rule.objects.active()
        assert valid_rule in active_rules

    def test_manager_active_does_not_return_future_rules(self, rule_factory):
        """Should not return rules which are scheduled to start in the future."""
        future_rule = rule_factory(
            date_start=maya.now().add(days=2).datetime(),
            date_end=maya.now().add(days=5).datetime(),
        )
        active_rules = Rule.objects.active()
        assert future_rule not in active_rules

    def test_manager_active_does_not_return_expired_rules(self, rule_factory):
        """Should not return rules whose date_end has passed."""
        expired_rule = rule_factory(
            date_start=maya.now().subtract(days=20).datetime(),
            date_end=maya.now().subtract(days=5).datetime(),
        )
        active_rules = Rule.objects.active()
        assert expired_rule not in active_rules

    def test_manager_active_returns_perpetual_rules(self, rule_factory):
        """Should return rules which have started, but have no defined end."""
        perpetual_rule = rule_factory(date_start=maya.now().datetime(), date_end=None)
        active_rules = Rule.objects.active()
        assert perpetual_rule in active_rules


@pytest.mark.django_db
class TestFeedRule:
    def test_match_against_feed(self, feed_rule, entry_factory):
        """Should only match corresponding feeds."""
        valid_entry = entry_factory(feed=feed_rule.feed)
        invalid_entry = entry_factory()
        assert feed_rule.match(valid_entry)
        assert not feed_rule.match(invalid_entry)

    def test_specific_returns_feed_rule(self, feed_rule):
        """Should return a FeedRule object when called on underlying Rule class."""
        assert feed_rule.specific == feed_rule
        assert feed_rule.rule_ptr.specific == feed_rule


@pytest.mark.django_db
class TestTextMatchRule:
    @pytest.mark.parametrize(
        "text_input, should_match",
        [["This is only a test", True], ["only", True], ["cowsay", False]],
    )
    def test_match_against_text(
        self, text_input, should_match, text_match_rule_factory, entry_factory
    ):
        """Should naively match text strings."""
        rule = text_match_rule_factory(text=text_input)
        entry = entry_factory(title="This is only a test.")
        is_match = rule.match(entry)
        assert is_match == should_match

    def test_specific_returns_text_match_rule(self, text_match_rule):
        """Should return a TextMatchRule object when called on underlying Rule class."""
        assert text_match_rule.specific == text_match_rule
        assert text_match_rule.rule_ptr.specific == text_match_rule
