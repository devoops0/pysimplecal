# pysimplecal
Sync caldav-events from remote URL and visualize them in simple html-page

# Requirements
* python3
* icalendar
* datetime
* pytz
* caldav

# Usage
In cal/sync.py update
* user
* password
* url
to match your needs.
Afterwards run
```
./sync.py
```
The resulting page will be placed in html/. Open html/calendar.html in your Browser to view the visualized events.
