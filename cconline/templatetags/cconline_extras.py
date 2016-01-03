__author__ = 'Filushin_DV'
from django import template
import string
import os
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from datetime import datetime

register = template.Library()


def active_link(url, val):
    if val in url:
        return 'class="active"'
    else:
        return ''


def trim_str(string_value):
    return string_value.rstrip(os.linesep).lstrip()


@register.filter(needs_autoescape=False)
def convertcrlf(string_value, autoescape=True):
    return mark_safe(string_value.replace("\n", "<br>"))


def addcss(field, css):
   return field.as_widget(attrs={"class": css})


register.filter('active_link', active_link)
register.filter('trim_str', trim_str)
register.filter('ccrlf', convertcrlf)
register.filter('addcss', addcss)

