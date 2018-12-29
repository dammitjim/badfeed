from django import template

register = template.Library()


@register.inclusion_tag("feeds/tags/pin_button.html", takes_context=True)
def pin_button(context, entry):
    return {"is_pinned": entry.is_pinned_by(context["request"].user), "entry": entry}


@register.inclusion_tag("feeds/tags/save_button.html", takes_context=True)
def save_button(context, entry):
    return {"is_saved": entry.is_saved_by(context["request"].user), "entry": entry}


@register.inclusion_tag("feeds/tags/watch_button.html", takes_context=True)
def watch_button(context, feed):
    return {"is_watched": feed.is_watched_by(context["request"].user), "feed": feed}


@register.inclusion_tag("feeds/tags/delete_button.html", takes_context=True)
def delete_button(context, entry):
    return {"is_deleted": entry.is_deleted_by(context["request"].user), "entry": entry}
