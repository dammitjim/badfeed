from typing import List

from badfeed.feeds.models import Entry
from badfeed.users.models import BadFeedUser


def delete_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_deleted(user) for entry in entries]


def pin_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_pinned(user) for entry in entries]


def save_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_saved(user) for entry in entries]
