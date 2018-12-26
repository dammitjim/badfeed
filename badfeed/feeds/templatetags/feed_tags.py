from django import template

register = template.Library()


@register.inclusion_tag("feeds/tags/pin_button.html", takes_context=True)
def pin_button(context, entry):
    return {"is_pinned": entry.is_pinned_by(context["request"].user), "entry": entry}


@register.inclusion_tag("feeds/tags/save_button.html", takes_context=True)
def save_button(context, entry):
    return {"is_saved": entry.is_saved_by(context["request"].user), "entry": entry}
