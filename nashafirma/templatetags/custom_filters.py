from django import template

register = template.Library()


@register.filter
def before_last_slash(value):
    return value.rsplit('/', 1)[0]
