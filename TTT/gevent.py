from __future__ import print_function
import gcred
import datetime
from dateutil.parser import parse
import httplib2
import os

class Event(gcred.GCredentials):
    """Get and set Google calendar event"""
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def get_events(self):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='m7sjghrgistm96tfh3og9nqm0k@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        
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

