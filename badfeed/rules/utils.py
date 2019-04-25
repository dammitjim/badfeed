from typing import List

from badfeed.feeds.models import Entry
from badfeed.rules.models import Rule


def apply_rules(entry: Entry, rules: List[Rule]):
    for rule in rules:
        concrete_rule = rule.specific()
        if not concrete_rule.match(entry):
            continue
        concrete_rule.apply(entry)
