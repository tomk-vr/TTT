
from __future__ import print_function
import tttEvent
import datetime
import importCsv
import gsheet
import pdfWriter

def main():
    """Shows basic usage of the Google Calendar API.
       Creates a Google Calendar API service object.
    """

    #LOGGING best practice
    #https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/


    evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                            cfname='calendar-python-quickstart.json',
                            sfname='client_secret.json')
    #sht = gsheet.Sheet()

    ### Print range sheet
    ### Insert new event
    #start = datetime.datetime(2018, 3, 3, 13, 0, 0)
    #end = datetime.datetime(2018, 3, 3, 18, 0, 0)
    #det = {'summary' : 'prova1'}
    #evt.set_event(start, end, summary='prova1')

    ### Import time track from csv timesheet e create related Events
    #imp = importCsv.ImportCsv()
    #imp.importData()

    ### get Events
    events = evt.get_events(month=2)
    ret = evt.get_data(events)
    print ('---------------')
    
    ### get HOURS MONTH
    #tot = float(evt.get_totHoursEvent(2))

    ### upadate gsheet
    #sht.update_sheet('Ore', '2018', 2, [tot])

    ### set HOURS MONTH
    #evt.get_totHoursEvent(1)

    ### set IN
    #evt.get_totHoursEvent(2)

    #page_token = None
    #while True:
    #  calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #  for calendar_list_entry in calendar_list['items']:
    #    print (calendar_list_entry['summary'], calendar_list_entry['id'])
    #  page_token = calendar_list.get('nextPageToken')
    #  if not page_token:
    #    break

    ### pdfWriter
    pdfw = pdfWriter.pdfWriter(r"c:\temp\test_report_lab.pdf")
    ret['pevts'].insert(0,['G', 'entrata', 'uscita', 'entrata', 'uscita', 'Pres'])
    pdfw.write_table(ret['pevts'])

if __name__ == '__main__':
    main()