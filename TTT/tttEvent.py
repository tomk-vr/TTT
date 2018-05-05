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
        print("HOURS MONTH %.2f" % (ret['totHours']))
        start = end.replace(hour=23, minute=0, second=0)
        end = end.replace(hour=23, minute=30, second=0)
        self.set_event(start, end, summary='ORE MESE', description=ret['totHours'])
 
    def print_events(self, events):
        if not events:  
            print('No upcoming events found.')
        
        ret = self.get_data(events)

        for pevt in ret['pevts']:
            print('{}: IN {}  OUT {} - IN {}  OUT {}  TOT: {}'.format(pevt[0], pevt[6], pevt[7], pevt[8], pevt[9], pevt[1]))

        print()
        print("HOURS MONTH %.2f" % (ret['totHours']))
        return ret

    def get_data (self, events):
        if not events:
            print('No upcoming events found.')

        retevts = []
        pevents = {}
        evt = []
        prevdt = ''
        hday = 0.0
        hours = 0.0
        permHours = 0.0
        month = 0
        year = 0
        for event in events:
            if event['summary'] == "ORE MESE":
                continue
            startdt = parse(event['start']['dateTime'])
            enddt = parse(event['end']['dateTime'])
            span = enddt - startdt
            month = startdt.month
            year = startdt.year
            if startdt.strftime("%d/%m/%Y") == prevdt:
                hday += span.total_seconds()
                hh = hday/3600
                hm = math.floor(hh*4)/4
                hours += hm
                evt[1] = str(hm)
                if hm - 8 < 0:
                    evt[2] = 8 - hm
                    permHours += 8 - hm
                evt.extend([startdt.strftime("%H:%M"), enddt.strftime("%H:%M")])
                pevents[startdt.day] = evt
                hday = 0.0
            else:
                if hday != 0.0:
                    hours += hm
                    pevents[startdt.day] = evt
                    if hm - 8 < 0:
                        evt[2] = 8 - hm
                        permHours += 8 - hm
                
                hday = span.total_seconds()
                hh = hday/3600
                hm = math.floor(hh*4)/4
                prevdt = startdt.strftime("%d/%m/%Y")
                #startdt.strftime("%d/%m/%Y")
                evt = [startdt.day, str(hm), '', '', '', '', startdt.strftime("%H:%M"), enddt.strftime("%H:%M")]


        hols = {}
        holidays = self.get_holidays(year, month)
        for hol in holidays:
            holiday = parse(hol['start']['date'])
            if holiday.month == month:
                hols[hol.day] = hol 

        for dd in range(1, calendar.monthrange(year, month)[1]+1):
            if dd in pevents:
                retevts.append(pevents[dd])
            else:
                today = datetime.datetime(year, month, dd)
                if today.weekday() > 4 or today.day in hols:
                    #Saturday or Sunday
                    retevts.append([dd, '', '', '', '', '', '', '', '', ''])
                else:
                    retevts.append([dd, '', '8', '', '', '', '', '', '', ''])
                    permHours += 8

        ret = { 'pevts': retevts, 'totHours': hours, 'permHours' : permHours }
        return ret
        #ARROTONDA.DIFETTO(( (ORARIO(ORA(C23);MINUTO(C23);SECONDO(C23)) - ORARIO(ORA(B23);MINUTO(B23);SECONDO(B23)) )+ (ORARIO(ORA(E23);MINUTO(E23);SECONDO(E23)) - ORARIO(ORA(D23);MINUTO(D23);SECONDO(D23)))) * 24; 0,25)
