
from __future__ import print_function
import gevent
import datetime

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    evt = gevent.Event()

    start = datetime.datetime(2018, 3, 3, 13, 0, 0)
    end = datetime.datetime(2018, 3, 3, 18, 0, 0)
    det = {'summary' : 'prova1'}
    evt.set_event(start, end, summary='prova1')

    evt.get_events()

    #page_token = None
    #while True:
    #  calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #  for calendar_list_entry in calendar_list['items']:
    #    print (calendar_list_entry['summary'], calendar_list_entry['id'])
    #  page_token = calendar_list.get('nextPageToken')
    #  if not page_token:
    #    break

if __name__ == '__main__':
    main()