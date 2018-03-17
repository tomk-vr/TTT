import csv
import time
import datetime
import locale
import gevent

class ImportCsv(object):
    """Import csv timesheet and create an 2 events foreach row"""
    def importData(self):
        locale.setlocale(locale.LC_TIME, "it")
        evt = gevent.Event()

        with open('C:\\Users\\ivan.pernigo\\AppData\\Local\\PythonProject\\TTT\\gen_2018.csv') as csvfile:
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
                    evt.set_event(start, end, summary='pomeriggio')
                except ValueError:
                    print("")



