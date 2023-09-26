from django import template
from django.utils.safestring import mark_safe
from markdown import markdown


register = template.Library()


@register.filter
def marked(text):
    return mark_safe(markdown(text))
