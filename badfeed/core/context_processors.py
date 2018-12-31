from django.http import HttpRequest


def search_term_processor(request: HttpRequest):
    """Loads the search term into the template context, this is so we can display it in the search form."""
    return {"search_term": request.GET.get("term", default="")}
