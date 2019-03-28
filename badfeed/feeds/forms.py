from django import forms


class FeedActionsForm(forms.Form):
    ACTIONS_ARCHIVE = "archive"
    ACTIONS_HIDE = "hide"
    ACTIONS = [
        (ACTIONS_ARCHIVE, "Archive all feed entries"),
        (ACTIONS_ARCHIVE, "Hide feed for now"),
    ]
    action = forms.ChoiceField(choices=ACTIONS)
