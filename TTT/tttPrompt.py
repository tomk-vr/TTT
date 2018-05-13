from __future__ import print_function
import tttEvent
import datetime
import importCsv
import gsheet
import pdfWriter
import locale
import calendar
from cmd import Cmd

class tttPrompt(Cmd):
    """TTT prompt class"""

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print ("Hello, %s" % name)

    def do_import(self, args):
        """Import time track from csv timesheet e create related calendar events. Eg: import 'c:\march.csv'"""
        imp = importCsv.ImportCsv()
        imp.importData(args)

    def do_geth(self, args):
        """View tot hour in month. Eg: geth 3 returns March tot hours"""
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.get_totHoursEvent(int(args))

    def do_report(self, args):
        """Create time tracking pdf report"""

        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        now = datetime.datetime.now()
        monthInt = 2
        events = evt.get_events(month=monthInt)
        ret = evt.print_events(events)
        print ('---------------')

        ### pdfWriter
        pdfw = pdfWriter.pdfWriter(r"c:\temp\test_report_lab.pdf")
    
        pdfw.write_header('Consuntivo mensile Ivan Pernigo (Moxlab)')
        locale.setlocale(locale.LC_TIME, "it")
        monthStr = calendar.month_name[monthInt];
        pdfw.write_header('Mese: ' + monthStr + ' ' + str(now.year))
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        pdfw.write_header('Auto: propia = P ; non propia = NP', 'Normal')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        ret['pevts'].insert(0,['G', 'Pres', 'Perm', 'Trasferta', 'Auto', 'Pernotto', 'Entrata', 'Uscita', 'Entrata', 'Uscita'])
        ret['pevts'].append(['Tot', 'Ore', 'Perm', '', '', '', '', '', '', ''])
        ret['pevts'].append(['', ret['totHours'], ret['permHours'], '', '', '', '', '', '', ''])
        pdfw.write_table(ret['pevts'])
        pdfw.build()

    def do_quit(self, args):
        """Quits TTT."""
        print ("Quitting.")
        raise SystemExit


if __name__ == '__main__':
    prompt = tttPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting TTT prompt...')
