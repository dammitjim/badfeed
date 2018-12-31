from badfeed.feeds.models import EntryState


def delete_entries_for_user(entries, user):
    return [EntryState.objects.create(entry=entry, user=user, state=EntryState.STATE_DELETED) for entry in entries]


def pin_entries_for_user(entries, user):
    return [EntryState.objects.create(entry=entry, user=user, state=EntryState.STATE_PINNED) for entry in entries]


def save_entries_for_user(entries, user):
    return [EntryState.objects.create(entry=entry, user=user, state=EntryState.STATE_SAVED) for entry in entries]
