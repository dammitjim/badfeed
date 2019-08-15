from django.conf import settings
from django.http import HttpRequest


def search_term_processor(request: HttpRequest):
    """Load the search term into the template context.

    This is so we can display it in the search form.
    """
    return {"search_term": request.GET.get("term", default="")}


def global_context(request: HttpRequest):
    """Set constants into the global template context."""
    return {"debug": settings.DEBUG}
