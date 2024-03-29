
from django.template import Library
register = Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='as_dict')
def as_dict(value):
    return vars(value)
