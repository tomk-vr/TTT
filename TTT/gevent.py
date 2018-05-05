from __future__ import print_function
import gcred
import datetime
import httplib2
import math
import calendar
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

    def update_event(self, event):

        updated_event = self.service.events().update(calendarId=self.CALID, eventId=event['id'], body=event).execute()

        # Print the updated date.
        print (updated_event['updated'])

    def print_events(self, events):
        if not events:  
            print('No upcoming events found.')
        
        for event in events:
            startdt = parse(event['start']['dateTime'])
            enddt = parse(event['end']['dateTime'])
            span = enddt - startdt
            print(startdt.strftime("%d/%m/%Y"))
            print('{}:  IN {}    OUT {}     TOT:{}'.format(event['summary'], startdt.strftime("%H:%M:%S"), enddt.strftime("%H:%M:%S"), span))

    def get_holidays(self, year, month):
        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)
        eventsResult = self.service.events().list(
            calendarId='it.italian#holiday@group.v.calendar.google.com', timeMin=start.isoformat() + 'Z', timeMax=end.isoformat() + 'Z', 
            maxResults=80, singleEvents=True,
            orderBy='startTime').execute()
        holidays = eventsResult.get('items', [])
        return holidays