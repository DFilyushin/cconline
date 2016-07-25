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
        tag_name, year, month, event_list, show_next, show_prev, id_history = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return EventCalendarNode(year, month, event_list, show_next, show_prev, id_history)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list, showNext, showPrev, id_history):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
            self.showNext = template.Variable(showNext)
            self.showPrev = template.Variable(showPrev)
            self.id_history = template.Variable(id_history)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            isShowPrevLink = self.showPrev.resolve(context)
            isShowNextLink = self.showNext.resolve(context)
            idHistory = self.id_history.resolve(context)
            cal = EventCalendar(my_event_list, isShowPrevLink, isShowNextLink, idHistory)
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

    def __init__(self, events, IsPrev, IsNext, idHistory):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)
        self.show_next_month = IsNext
        self.show_prev_month = IsPrev
        self.idHistory = idHistory

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = []
                for event in self.events[day]:
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append('<img src="/static/images/dummy-small.png">')
                    body.append('</a>')
                return self.day_cell(cssclass, '<span class="dayNumber"><a href="%s">%d</span>' % (event.get_absolute_url(), day))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

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
        if self.month == 1:
            prev_month = 12
            prev_year = self.year - 1
        else:
            prev_month = self.month - 1
            prev_year = self.year

        if self.month == 12:
            next_month = 1
            next_year = self.year + 1
        else:
            next_month = self.month + 1
            next_year = self.year
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table table-condensed">')
        a('<tr>')
        a('<td colspan="2" align="center">')
        if self.show_prev_month:
            a('<a href="/medication/list_by_date/%i/?year=%i&month=%i">%s' % (self.idHistory, prev_year, prev_month, named_month(prev_month)))
        a('</td>')
        a('<td colspan="3" align="center">')
        a(named_month(month))
        a('</td>')
        a('<td colspan="2" align="center">')
        if self.show_next_month:
            a('<a href="/medication/list_by_date/%i/?year=%i&month=%i">%s' % (self.idHistory, next_year, next_month, named_month(next_month)))
        a('</td>')
        a('</tr>')
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