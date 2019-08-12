from django.db.models import Count, Max, Q

from feedzero.feeds.models import Entry, EntryState, Feed
from feedzero.users.models import FeedZeroUser


def feeds_by_last_updated_entry(user):
    """Load watched feeds, ordered by when their entries were last published.

    The query we return must match the following conditions:

    * The feed must have 1 or more entries
    * The feed must have 1 or more unread entries for this user
        where an unread entry is one without a state
    * The entries must be ordered by date published
    * Fully actioned feeds must not be returned.
    """
    qs = (
        Feed.objects.watched_by(user)
        .filter(entries__gt=0)
        .annotate(
            actioned_entries=Count(
                "entries__states", filter=Q(entries__states__user=user)
            )
        )
        .annotate(last_published=Max("entries__date_published"))
        .order_by("-last_published")
    )

    # TODO figure out how to make this a part of the above query
    # for now, we are cheeky and exclude any feeds whereby the
    # amount of actioned entries is equal to the amount of entries
    # (meaning there are no more entries to action)
    for feed in qs:
        if feed.actioned_entries >= feed.entries.count():
            qs = qs.exclude(pk=feed.pk)

    return qs


def get_actionable_entries(feed, user):
    """Load the 5 latest unread / unactioned entries for the feed."""
    return feed.entries(manager="user_state").unread(user).order_by("-date_published")


def apply_state_to_entry(entry: Entry, state: str, for_user: FeedZeroUser):
    if state == EntryState.STATE_READ:
        entry.mark_read_by(for_user)
    elif state == EntryState.STATE_SAVED:
        entry.mark_saved(for_user)
    elif state == EntryState.STATE_PINNED:
        entry.mark_pinned(for_user)
    elif state == EntryState.STATE_DELETED:
        entry.mark_deleted(for_user)
