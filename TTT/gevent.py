from __future__ import print_function
import gcred
import datetime
import calendar
import httplib2
import math

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

    def set_in(self, delta):
        now = datetime.datetime.now()
        now = now + datetime.timedelta(minutes=delta)

        start = datetime.datetime(now.year, now.month, now.day)
        end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        events = self.get_events(start=start, end=end)
        if len(events) > 1:
            print('ERROR: too many events')
            return

        if len(events) > 0:
            sum = 'pomeriggio'
        else:
            sum = 'mattina'

        self.set_event(now, now + datetime.timedelta(seconds=1), summary=sum)

    def set_out(self, delta):
        now = datetime.datetime.now()
        now = now + datetime.timedelta(minutes=delta)

        start = datetime.datetime(now.year, now.month, now.day)
        end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        events = self.get_events(start=start, end=end)
        if len(events) > 2:
            print('ERROR: too many events')
            return

        #Terminare con la modifica dell'evento mattina o pomeriggio usando event.update (vedi api)

        

    def set_totHoursEvent(self, month, year=None):
        now = datetime.datetime.now()
        if year == None:
            year = now.year

        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        events = self.get_events(start=start, end=end)
        day = datetime.date.min
        hday = 0.0
        hours = 0.0
        for event in events:
            if event['summary'] != "ORE MESE":
                dd = parse(event['start']['dateTime'])
                if day != datetime.date.min and day != dd.date():
                    hh = hday/3600
                    hm = math.floor(hh*4)/4
                    print (day.strftime("%d/%m/%Y"), ' ', hm);
                    hours += hm
                    hday = 0.0
                
                day = dd.date()
                startdt = parse(event['start']['dateTime'])
                enddt = parse(event['end']['dateTime'])
                hday += (enddt - startdt).total_seconds()

        hh = hday/3600
        hm = math.floor(hh*4)/4
        print (day.strftime("%d/%m/%Y"), ' ', hm);
        hours += hm
        print('HOURS MONTH : ', hours)
        start = end.replace(hour=23, minute=0, second=0)
        end = end.replace(hour=23, minute=30, second=0)
        self.set_event(start, end, summary='ORE MESE', description=hours)
        #ARROTONDA.DIFETTO(( (ORARIO(ORA(C23);MINUTO(C23);SECONDO(C23)) - ORARIO(ORA(B23);MINUTO(B23);SECONDO(B23)) )+ (ORARIO(ORA(E23);MINUTO(E23);SECONDO(E23)) - ORARIO(ORA(D23);MINUTO(D23);SECONDO(D23)))) * 24; 0,25)

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
