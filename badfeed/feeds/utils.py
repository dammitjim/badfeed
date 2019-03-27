from typing import List

from django.db.models import Count, Max, Q

from badfeed.feeds.models import Entry, Feed
from badfeed.users.models import BadFeedUser


def delete_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_deleted(user) for entry in entries]


def pin_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_pinned(user) for entry in entries]


def save_entries_for_user(entries: List[Entry], user: BadFeedUser):
    return [entry.mark_saved(user) for entry in entries]


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


def get_actionable_entries(feed, user, num=5):
    """Load the 5 latest unread / unactioned entries for the feed."""
    unread_entries = (
        feed.entries(manager="user_state").unread(user).order_by("-date_published")
    )
    return unread_entries[:num]
