#!/usr/bin/env python3

from datetime import datetime, date
import caldav
from caldav.elements import dav, cdav
from download import dl, cleanup
from cal_parser import parse
import re
import time

username = "user"   # caldav user
password = "password"   # relating password
url = "http://insert.your.url/here"        # caldav-URL


'''
lets the user choose the calendar, he wants to to get synced
@parasms:
    calendars: list
'''
def choose_cal(calendars):
    if not calendars:
        return 0

    for i, calendar in enumerate(calendars):
        print(i, ": ", calendar)

    choice = int(input("Choose a calendar to sync: "))
    return calendars[choice]


'''
Discovers all calendars for a given CalDav-URL,
downloads all events for the chosen calendar
and generates a simple HTML-page as overview
'''
def sync():
    cleanup()
    client = caldav.DAVClient(url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    print("Discovering calendars...")

    if len(calendars) > 0:
        calendar = choose_cal(calendars)
        print("Synchronizing Calendar....")
        for event in calendar.events():
            event_url = str(event)
            event_url = re.sub('^Event: ', '', event_url)
            dl(event_url, username, password)
    print("Generating overview....")
    overview_page = parse()
    print("Done!")

if __name__ == "__main__":
    sync()
