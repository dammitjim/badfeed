from django import forms


class FeedActionsForm(forms.Form):
    ACTIONS_NOTHING = "na"
    ACTIONS_ARCHIVE = "archive_all"
    ACTIONS = [(ACTIONS_NOTHING, "---"), (ACTIONS_ARCHIVE, "Archive all feed entries")]
    action = forms.ChoiceField(choices=ACTIONS)


class EntryActionsForm(forms.Form):
    ACTIONS_NOTHING = "na"
    ACTIONS_ARCHIVE = "archive_older"
    ACTIONS = [
        (ACTIONS_NOTHING, "---"),
        (ACTIONS_ARCHIVE, "Archive all entries older than this entry"),
    ]
    action = forms.ChoiceField(choices=ACTIONS)
