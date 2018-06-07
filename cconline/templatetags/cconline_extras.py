__author__ = 'Filushin_DV'
from django import template
import string
import os
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import datetime


register = template.Library()

DEFAULT_LOGO = 'default.svg'

holidays = {
    '0101': 'christmas.svg',
    '0102': 'christmas.svg',
    '0308': '8-marta.svg',
    '0321': 'first_may.svg',
    '0322': 'first_may.svg',
    '0323': 'first_may.svg',
    '0501': 'first_may.svg',
    '0507': 'vvs.svg',
    '0509': 'vov.svg',
    '0617': 'nurse.svg',
    '0830': 'endepend.svg',
    '0706': 'astana.svg',
    '1201': 'endepend.svg',
    '1216': 'endepend.svg',

}


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


@register.simple_tag(name='link')
def jump_link():
    today = datetime.datetime.now()
    str_today = today.strftime('%m%d')
    return holidays.get(str_today, DEFAULT_LOGO)

register.filter('active_link', active_link)
register.filter('trim_str', trim_str)
register.filter('ccrlf', convertcrlf)
register.filter('addcss', addcss)
