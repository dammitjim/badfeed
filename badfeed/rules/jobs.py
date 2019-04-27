from typing import List

from django.contrib.auth import get_user_model
from django_rq import job

from badfeed.feeds.models import Entry
from badfeed.rules.models import Rule


User = get_user_model()


@job
def process_rules_for_user(user: User):
    entries = Entry.user_state.unread(user)
    rules = Rule.objects.active().filter(user=user)
    for entry in entries:
        apply_rules(entry, rules)


def apply_rules(entry: Entry, rules: List[Rule]):
    for rule in rules:
        concrete_rule = rule.specific()
        if not concrete_rule.match(entry):
            continue
        concrete_rule.apply(entry)
