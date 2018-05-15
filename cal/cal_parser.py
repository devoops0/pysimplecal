#!/usr/bin/env python3

from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
import os
import sys

'''
Iterates over a folder of ics-files and parses the files for events.
It then collects all events in a single list, where they are filtered
for the type 'VEVENT' and then sorted bei their start-date.
At last, a simple HTML-page is generated to give an overview of the events.
'''

def parse():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_dir = os.path.join(root_dir, 'html/')
    events_dir = os.path.join(root_dir, 'events/')
    event_files = []
    events = []

    for f in os.listdir(events_dir):
        if(os.path.isfile(os.path.join(events_dir,f))):
            event_files.append(f)

    template = open(os.path.join(html_dir, 'head.html'), 'r')
    header = template.read()
    template.close()

    html = open(os.path.join(html_dir, 'calendar.html'), 'w+')
    html.write(header)

    for event_file in event_files:
        f = open(os.path.join(events_dir,event_file), 'rb')
        c = Calendar.from_ical(f.read())
        for comp in c.walk('VEVENT'):
            events.append(comp)
        f.close()

    events = filter(lambda c: c.name=='VEVENT', events)
    events = sorted(events,
            key=lambda c: datetime(
                c.get('dtstart').dt.year, c.get('dtstart').dt.month, c.get('dtstart').dt.day),
            reverse=False)

    counter = 0
    for event in events:
        if(counter%2 != 0):
            html.write('<div class="row">\n')
        html.write('<div class="col-xs-2 col-md-2 col-ld-2">')
        html.write("</div>")
        html.write('<div class=\"grow cal-entry col-xs-4 col-md-4 col-ld-4"> \n')
        html.write("<p>" + event.get('summary') + "</p>\n")
        html.write("<p>von: " + "{:%d.%m.%y, %H:%M Uhr}".format(event.get('dtstart').dt) + "</p>\n")
        html.write("<p>Bis: " + "{:%d.%m.%y, %H:%M Uhr}".format(event.get('dtend').dt) + "</p>\n")
        html.write("</div>")
        html.write('<div class="col-xs-2 col-md-2 col-ld-2">')
        html.write("</div>")
        if(counter%2 != 0):
            html.write("</div>")
        counter += 1

    html.write("</div>")
    html.write('</body>\n')
    html.close()
    return os.path.join(html_dir, 'calendar.html')

if __name__ == '__main__':
    parse()
