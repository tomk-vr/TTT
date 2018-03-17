from __future__ import print_function
import gcred
import datetime
import calendar
import httplib2

from apiclient import discovery
from dateutil.parser import parse

class Event(gcred.GCredentials):
    """Get and set Google calendar event"""

    CALID = 'm7sjghrgistm96tfh3og9nqm0k@group.calendar.google.com'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'calendarId' in kwargs:
            self.CALID = kwargs['calendarId']
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def get_events(self, **period):
        now = datetime.datetime.now()
        if 'year' in period:
            year = period['year']
        else:
            year = now.year

        if 'month' in period:
            start = datetime.datetime(year, period['month'], 1)
            end = datetime.datetime(year, period['month'], calendar.monthrange(year, period['month'])[1], 23, 59, 59)
        elif 'start' in period:
            start =period['start']
            if 'end' in period:
                end = period['end']
            else:
                end = datetime.datetime(year, period['month'], calendar.monthrange(year, month)[1], 23, 59, 59) 

        print('Getting events between: {} and {}'.format(start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y")))
        eventsResult = self.service.events().list(
            calendarId=self.CALID, timeMin=start.isoformat() + 'Z', timeMax=end.isoformat() + 'Z', 
            maxResults=80, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        return events
    
    def get_totHoursEvent(self, month, year=None):
        now = datetime.datetime.now()
        if year == None:
            year = now.year

        start = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        events = self.get_events(start=start, end=end)
        for event in events:
            if event['summary'] == "ORE MESE":
                print ('{}   tot: {}'.format(calendar.month_name[month], event['description']))

    def set_event(self, start, end, **details):
        event = {
          'summary': details.get('summary', ''),
          'location': details.get('location', ''),
          'description': details.get('description', ''),
          'start': {
            'dateTime': start.astimezone().isoformat(),
            #'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': end.astimezone().isoformat()
            #'timeZone': 'America/Los_Angeles',
          },
          #'recurrence': [
          #  'RRULE:FREQ=DAILY;COUNT=2'
          #],
          #'attendees': [
          #  {'email': 'lpage@example.com'},
          #  {'email': 'sbrin@example.com'},
          #],
          #'reminders': {
          #  'useDefault': False,
          #  'overrides': [
          #    {'method': 'email', 'minutes': 24 * 60},
          #    {'method': 'popup', 'minutes': 10},
          #  ],
          #},
        }

        event = self.service.events().insert(calendarId=self.CALID, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    def print_events(self, events):
        if not events:
            print('No upcoming events found.')
        
        hmonth = datetime.timedelta()
        for event in events:
            if event['summary'] == "ORE MESE":
                continue
            startdt = parse(event['start']['dateTime'])
            enddt = parse(event['end']['dateTime'])
            span = enddt - startdt
            hmonth += span
            print(startdt.strftime("%d/%m/%Y"))
            print('{}:  IN {}    OUT {}     TOT:{}'.format(event['summary'], startdt.strftime("%H:%M:%S"), enddt.strftime("%H:%M:%S"), span))

        print()
        print("HOURS MONTH %.2dh: %.2dm: %.2ds" % (((hmonth.days * 24) + hmonth.seconds//3600),(hmonth.seconds//60)%60, hmonth.seconds%60))
