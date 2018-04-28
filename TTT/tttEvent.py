import gevent
import httplib2
import datetime
import calendar
import math
import locale

from apiclient import discovery
from dateutil.parser import parse

class TTTEvent(gevent.Event):
    """manage TTT gcal event """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'calendarId' in kwargs:
            self.CALID = kwargs['calendarId']
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def set_in(self, delta):
        now = datetime.datetime.now()
        now = now + datetime.timedelta(minutes=delta)

        print ('TTTEvent.set_in ', now.strftime("%d/%m/%Y %H:%M:%S"))
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

        print ('TTTEvent.set_out ', now.strftime("%d/%m/%Y %H:%M:%S"))
        start = datetime.datetime(now.year, now.month, now.day)
        end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        events = self.get_events(start=start, end=end)
        if len(events) > 2:
            print('ERROR: too many events')
            return

        if len(events) == 0:
            print('ERROR: no IN events')
            return

        event = events[len(events) - 1]
        super().print_events([event])
        event['end']['dateTime'] = now.astimezone().isoformat()
        print ('UPDATING')
        super().print_events([event])
        self.update_event(event)
      
    def get_totHoursEvent(self, month, year=None):
        now = datetime.datetime.now()
        if year == None:
            year = now.year

        locale.setlocale(locale.LC_TIME, "it")
        print ('TTTEvent.get_totHoursEvent ', calendar.month_name[month], ' ', year)

        start = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        events = self.get_events(start=start, end=end)
        for event in events:
            if event['summary'] == "ORE MESE":
                print ('{}   tot: {}'.format(calendar.month_name[month], event['description']))
        return event['description']
                      
    def set_totHoursEvent(self, month, year=None):
        now = datetime.datetime.now()
        if year == None:
            year = now.year

        locale.setlocale(locale.LC_TIME, "it")
        print ('TTTEvent.set_totHoursEvent ', calendar.month_name[month], ' ', year)
        
        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        events = self.get_events(start=start, end=end)
        ret = self.get_data(events)
        print("HOURS MONTH %.2f" % (ret['tothours']))
        start = end.replace(hour=23, minute=0, second=0)
        end = end.replace(hour=23, minute=30, second=0)
        self.set_event(start, end, summary='ORE MESE', description=ret['tothours'])
 
    def print_events(self, events):
        if not events:  
            print('No upcoming events found.')
        
        ret = self.get_data(events)

        for pevt in ret['pevts']:
            print('{}: IN {}  OUT {} - IN {}  OUT{}  TOT: {}'.format(pevt[0], pevt[1], pevt[2], pevt[3], pevt[4], pevt[5]))

        print()
        print("HOURS MONTH %.2f" % (ret['tothours']))

    def get_data (self, events):
        if not events:
            print('No upcoming events found.')

        pevents = []
        evt = []
        prevdt = ''
        hday = 0.0
        hours = 0.0
        for event in events:
            if event['summary'] == "ORE MESE":
                continue
            startdt = parse(event['start']['dateTime'])
            enddt = parse(event['end']['dateTime'])
            span = enddt - startdt
            hday += span.total_seconds()
            if startdt.strftime("%d/%m/%Y") == prevdt:
                hh = hday/3600
                hm = math.floor(hh*4)/4
                hours += hm
                evt.extend([startdt.strftime("%H:%M"), enddt.strftime("%H:%M"), str(hm)])
                pevents.append(evt)
                hday = 0.0
            else: 
                prevdt = startdt.strftime("%d/%m/%Y")
                evt = [startdt.strftime("%d/%m/%Y"), startdt.strftime("%H:%M"), enddt.strftime("%H:%M")]

        ret = { 'pevts': pevents, 'tothours': hours }
        return ret
        #ARROTONDA.DIFETTO(( (ORARIO(ORA(C23);MINUTO(C23);SECONDO(C23)) - ORARIO(ORA(B23);MINUTO(B23);SECONDO(B23)) )+ (ORARIO(ORA(E23);MINUTO(E23);SECONDO(E23)) - ORARIO(ORA(D23);MINUTO(D23);SECONDO(D23)))) * 24; 0,25)
