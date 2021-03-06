# may need to pip install icalendar
from datetime import datetime, timedelta, date
from icalendar import Calendar, Event
import requests
import pprint
import pytz
import cgi
pp = pprint.PrettyPrinter()

request = requests.get('https://calendar.google.com/calendar/ical/m2t9ena5lcnh28dot8f515mf6s%40group.calendar.google.com/public/basic.ics')
# print request.text

cal = Calendar.from_ical(request.text)

def separate_pretty_datetime(dt):
    return dt.strftime('%A %-d %B') + pretty_time_part(dt)

# appends to formatted date
def pretty_time_part(dt):
    if dt.hour == 0 and dt.minute == 0:
        return ''
    elif dt.minute == 0:
        return dt.strftime(', %-I%p')
    else:
        return dt.strftime(', %-I.%M%p')
    
def pretty_date_range(startdate, enddate):
    # want to:
    # only show minutes if not zero
    # only show end date if differs from start
    # test with day called wonder
    if startdate.strftime('%d %m %Y') == enddate.strftime('%d %m %Y'): # same day
        datestring = startdate.strftime('%A %-d %B') # start date always included

        # add AM/PM if ambiguous
        if(enddate.hour - startdate.hour >= 12): # could be ambiguous
            return datestring + startdate.strftime(', %-I%p') + enddate.strftime('-%-I%p')
        else:
            return datestring + startdate.strftime(', %-I') + enddate.strftime('-%-I%p')
    else: # different days (or midnight to midnight)
        print 'enddate',enddate, type(enddate)
        print 'startdate',startdate
        if(type(startdate) == date):
            # print 'converting startdate to datetime'
            startdate = datetime(startdate.year, startdate.month, startdate.day)
        if(type(enddate) == date):
            # print 'converting enddate to datetime'
            enddate = datetime(enddate.year, enddate.month, enddate.day)
        if startdate.hour == 0 and startdate.minute == 0 and enddate.hour == 0 and enddate.minute == 0: #whole days
            if startdate.month != enddate.month: # across months
                datestring = startdate.strftime('%-d %B - ') + enddate.strftime('%-d %B')
            elif enddate.day == (startdate.day + 1): # one day
                datestring = startdate.strftime('%A %-d %B')
            else: # whole number of days within a single month (assuming same year!)
                td = timedelta(1)
                datestring = startdate.strftime('%-d-') + (enddate - td).strftime('%-d %B')
        else: # different days, timed start and end
            datestring = startdate.strftime('%-d %B') + pretty_time_part(startdate) + ' - ' + enddate.strftime('%-d %B') + pretty_time_part(enddate)
            
        return datestring

def load():
    events = []
    for event in cal.walk():
        new_event = {}
        print event
    #     print type(event)
        if(type(event) == Event):
            new_event['startdate'] = event.decoded('dtstart')
            new_event['enddate'] = event.decoded('dtend')
            new_event['lastmod'] = event.decoded('last-modified')
            new_event['summary'] = event['SUMMARY']
            if event['LOCATION']:
                new_event['location'] = event['LOCATION']

            if event['DESCRIPTION'].startswith(event['SUMMARY']):
                new_event['description'] = cgi.escape(event['DESCRIPTION'][len(event['SUMMARY']):]) + '\n'
            else:
                new_event['description'] = event['DESCRIPTION'] + '\n'
            new_event['lastmod'] = event['lastmod']
            events.append(new_event);
    return events

def output():
    out = ""
    # sort London timezone
    tzi = pytz.UTC
    for event in cal.walk():
        print event
    #     print type(event)
        if(type(event) == Event):
            startdate = event.decoded('dtstart')
            enddate = event.decoded('dtend')
            lastmod = event.decoded('last-modified')
            if type(enddate) == date:
                enddate = datetime(enddate.year, enddate.month, enddate.day).replace(tzinfo=tzi)
            if enddate > (datetime.now().replace(tzinfo=tzi)):
                out += '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'

                # print type(startdate)
                out += '<strong>'+event['SUMMARY'] + '</strong>\n'
                # print startdate, enddate
                out += pretty_date_range(startdate, enddate) + '\n'
                if event['LOCATION']:
                    out += '@ ' + event['LOCATION'] + '\n'

                if event['DESCRIPTION'].startswith(event['SUMMARY']):
                    out += cgi.escape(event['DESCRIPTION'][len(event['SUMMARY']):]) + '\n'
                else:
                    out += event['DESCRIPTION'] + '\n'
                out += '<small>' + separate_pretty_datetime(lastmod) + '</small>'

    return out.replace('\n', '<br />')
            