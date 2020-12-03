from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='get')
def get(d, k):
    return d.get(k, None)


@register.filter(name='index')
def index(array, i):
    return array[i]


@register.filter(name='trunc')
def trunc(string, num):
    try:
        return round(float(string), num)
    except ValueError:
        return string


@register.filter(name='split')
@stringfilter
def split(string, sep):
    return string.split(sep)
