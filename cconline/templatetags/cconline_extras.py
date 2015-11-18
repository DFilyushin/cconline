__author__ = 'Filushin_DV'
from django import template
import string
import os

register = template.Library()


def active_link(url, val):
    if val in url:
        return 'class="active"'
    else:
        return ''


def trim_str(string_value):
    return string_value.rstrip(os.linesep).lstrip()

register.filter('active_link', active_link)
register.filter('trim_str', trim_str)

