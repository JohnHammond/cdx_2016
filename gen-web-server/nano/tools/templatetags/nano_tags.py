# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from math import modf, floor, ceil

from django import template
from django.template.defaultfilters import stringfilter
 
from nano.tools import grouper
 
register = template.Library()
 
@register.filter
def startswith(value, arg):
    """Usage {% if value|startswith:"arg" %}"""
    if value:
        return value.startswith(arg)
    return False
startswith.is_safe = True

@register.filter
def endswith(value, arg):
    """Usage {% if value|endswith:"arg" %}"""
    if value:
        return value.endswith(arg)
    return False
endswith.is_safe = True

@register.filter
@stringfilter
def nbr(text):
    """Replace whitespace with non-breaking-space"""

    pieces = text.split()
    text = u'\xa0'.join(pieces)
    return text.encode('utf8')
nbr.is_safe = True

@register.filter
def partition(iterable, cols=4):
    "Split an iterable into columns"

    if not iterable:
        return ()
    try:
        cols = int(cols)
    except (ValueError, TypeError):
        return None
    the_tuple = tuple(iterable)
    maxrows = int(ceil(len(the_tuple)/float(cols)))
    columns = grouper(maxrows, the_tuple)
    return zip(*tuple(columns))
partition.is_safe = True

@register.filter
def integer(text):
    "Get integer-part of float"
    _, integer = modf(float(text))
    return str(int(integer))
integer.is_safe = True

@register.filter
def fraction(text, arg=1):
    "Get fractional part of float, pad with zeroes until <arg> length"
    arg = int(arg)
    fraction, _ = modf(float(text))
    integer, fraction = str(fraction).split('.', 1)
    lf = len(fraction)
    fraction = fraction[:arg]
    if arg > lf:
        fraction = u'%s%s' % (fraction, '0'*(arg-lf))
    return fraction
fraction.is_safe = True

@register.inclusion_tag('come_back.html', takes_context=True)
def come_back(context):
    """Turn current url path into a query-part for use in urls
    
    With default template: 
    
    If the path is stored in the context as /foo/bar, tag returns '?next=/foo/bar'
    """
    whereami = context.get('whereami')
    request = context.get('request')
    if request:
        path_info = request.META.get('PATH_INFO')
    return { 'come_back': whereami or path_info or '' }
