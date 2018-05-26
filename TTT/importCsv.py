import csv
import time
import datetime
import locale
import tttEvent

class ImportCsv(object):
    """Import csv timesheet and create an 2 events foreach row"""
    def importData(self, path=''):
        locale.setlocale(locale.LC_TIME, "it")
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        if path == '':
            csvpath = 'C:\\Users\\ivan.pernigo\\AppData\\Local\\PythonProject\\TTT\\marzo_2018.csv'
        else:
            csvpath = path

        with open(csvpath) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                try:
                    print(row[0])
                    data = datetime.datetime.strptime(row[0], "%d %B %Y")
                    tt = time.strptime(row[1], "%H:%M")
                    start = data.replace(hour=tt.tm_hour, minute=tt.tm_min)
                    tt = time.strptime(row[2], "%H:%M")
                    end = data.replace(hour=tt.tm_hour, minute=tt.tm_min)
                    print('    OK ', start, '       ', end)
                    evt.set_event(start, end, summary='mattina')

                    tt = time.strptime(row[3], "%H:%M")
                    start = data.replace(hour=tt.tm_hour, minute=tt.tm_min)
                    tt = time.strptime(row[4], "%H:%M")
                    end = data.replace(hour=tt.tm_hour, minute=tt.tm_min)
                    print('    OK ', start, '       ', end)
                    moreDict = {}
                    if row[11] != '':
                        moreDict['Trasferta'] = row[11]
                        moreDict['Spese'] = row[10]
                        moreDict['Pernotto'] = row[9]
                        descr = str(moreDict)
                    else:
                        descr = ''
                    evt.set_event(start, end, summary='pomeriggio', description=descr)
                except ValueError:
                    print("ImportCsv Error")



