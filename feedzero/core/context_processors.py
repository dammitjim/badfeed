from django.http import HttpRequest


def search_term_processor(request: HttpRequest):
    """Load the search term into the template context.

    This is so we can display it in the search form.
    """
    return {"search_term": request.GET.get("term", default="")}
