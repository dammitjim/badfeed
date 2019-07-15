import random


SPAFFY_QUOTES = [
    '"Then we are living in a place abandoned by God," I said, disheartened.',
    "Forgiveness means letting go of the hope for a better past.",
    "You've got to jump off cliffs all the time and build your wings on the way down.",
    "The sadness which reigned everywhere was but an excuse for unfailing kindness.",
    "No man can be an exile if he remembers that all the world is one city.",
    "Art is as useful as bread.",
    "All that blooms must fall.",
]


def get_spaffy_quote():
    """For when you need some text."""
    return random.choice(SPAFFY_QUOTES)
