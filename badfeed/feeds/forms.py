from django import forms


class FeedActionsForm(forms.Form):
    ACTIONS_NOTHING = "na"
    ACTIONS_ARCHIVE = "archive"
    ACTIONS_HIDE = "hide"
    ACTIONS = [
        (ACTIONS_NOTHING, "---"),
        (ACTIONS_ARCHIVE, "Archive all feed entries"),
        (ACTIONS_HIDE, "Hide feed for now"),
    ]
    action = forms.ChoiceField(choices=ACTIONS)
