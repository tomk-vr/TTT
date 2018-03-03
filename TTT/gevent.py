from __future__ import print_function
import gcred
import datetime
import httplib2

from dateutil.parser import parse
from apiclient import discovery

class Event(gcred.GCredentials):
    """Get and set Google calendar event"""

    CALID = 'm7sjghrgistm96tfh3og9nqm0k@group.calendar.google.com'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'calendarId' in kwargs:
            self.CALID = kwargs['calendarId']
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def get_events(self):
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = self.service.events().list(
            calendarId=self.CALID, timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        self.print_events(events)

    def set_event(self, start, end, **details):
        event = {
          'summary': details.get('summary', ''),
          'location': details.get('location', ''),
          'description': details.get('description', ''),
          'start': {
            'dateTime': start.isoformat() + 'Z',
            #'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': end.isoformat() + 'Z',
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
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, end, event['summary'])
            startdt = parse(event['start']['dateTime'])
            enddt = parse(event['end']['dateTime'])
            if isinstance(enddt, datetime.datetime):
               print ("stokaz")
            print(startdt, enddt, event['summary'])
            span = enddt - startdt
            print(span)
