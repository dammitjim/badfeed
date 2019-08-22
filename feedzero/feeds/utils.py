from feedzero.feeds.models import Entry, EntryState
from feedzero.users.models import FeedZeroUser


def apply_state_to_entry(entry: Entry, state: str, for_user: FeedZeroUser):
    if state == EntryState.STATE_READ:
        entry.mark_read_by(for_user)
    elif state == EntryState.STATE_SAVED:
        entry.mark_saved(for_user)
    elif state == EntryState.STATE_PINNED:
        entry.mark_pinned(for_user)
    elif state == EntryState.STATE_DELETED:
        entry.mark_deleted(for_user)
