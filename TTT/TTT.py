
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from dateutil.parser import parse

import gevent

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    #cred = gcred.GCredentials();
    #credentials = cred.get_credentials()
    evt = gevent.Event()
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