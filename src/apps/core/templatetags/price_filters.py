from django import template

register = template.Library()


@register.filter
def comma(value):
    try:
        value = int(value)
        return f"{value:,}"
    except:
        return value
