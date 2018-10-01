from .gcred import GCredentials
import datetime
import httplib2
from apiclient import discovery
import calendar
from .models import DayTime
from dateutil.parser import parse

class DBYearDate(GCredentials):
    """Fill DB with records for one year"""
    
    CALID = 'm7sjghrgistm96tfh3og9nqm0k@group.calendar.google.com'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'calendarId' in kwargs:
            self.CALID = kwargs['calendarId']
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def fillDB(self, year, purge=False):
        if purge:
            date = datetime.date(year=year, month=1, day=1)
            DayTime.objects.filter(day__gte=date).delete()

        for month in range(1,13):
            hols = {}
            holidays = self.get_holidays(year, month)
            for hol in holidays:
                holiday = parse(hol['start']['date'])
                print("holiday date " + hol['start']['date'])
                if holiday.month == month:
                    hols[holiday.day] = hol 

            for dd in range(1, calendar.monthrange(year, month)[1]+1):
                today = datetime.date(year=year, month=month, day=dd)
                if today.weekday() > 4 or today.day in hols:
                    DayTime.objects.create(day=today, hol=True)
                else:
                    DayTime.objects.create(day=today)
                 

    def get_holidays(self, year, month):
        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)
        eventsResult = self.service.events().list(
            calendarId='it.italian#holiday@group.v.calendar.google.com', timeMin=start.isoformat() + 'Z', timeMax=end.isoformat() + 'Z', 
            maxResults=80, singleEvents=True,
            orderBy='startTime').execute()
        holidays = eventsResult.get('items', [])
        return holidays


