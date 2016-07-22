# -*- coding: utf-8 -*-

from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby
import datetime

register = template.Library()


day_abbr = (u'Пн', u'Вт', u'Ср', u'Чт', u'Пт', u'Сб', u'Вс')
month_names = (u'Январь',u'Февраль',u'Март',u'Апрель',u'Май',u'Июнь',u'Июль',u'Август',u'Сентябрь',u'Октябрь',u'Нобябрь',u'Декабрь')

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return month_names[month_number-1]


def do_event_calendar(parser, token):
    """
    The template tag's syntax is {% event_calendar year month event_list %}
    """

    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return EventCalendarNode(year, month, event_list)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = EventCalendar(my_event_list)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return


class EventCalendar(HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = []
                for event in self.events[day]:
                    # body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append('<img src="/static/images/dummy-small.png">')
                    body.append('</a>')
                # body.append()
                # return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
                return self.day_cell(cssclass, '<span class="dayNumber"><a href="%s">%d</span>' % (event.get_absolute_url(), day))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    #def formatmonth(self, year, month):
    #    self.year, self.month = year, month
    #    return super(EventCalendar, self).formatmonth(year, month)
    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th class="%s">%s</th>' % (self.cssclasses[day], day_abbr[day])

    def formatmonth(self, year, month):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = year, month
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table table-condensed">')
        a('\n')
        a(named_month(month))
        a('\n')
        a(super(EventCalendar, self).formatweekheader())
        a('\n')
        for week in super(EventCalendar, self).monthdays2calendar(year, month):
            a(super(EventCalendar, self).formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def group_by_day(self, events):
        field = lambda event: event.dateapp.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to templates
register.tag("event_calendar", do_event_calendar)