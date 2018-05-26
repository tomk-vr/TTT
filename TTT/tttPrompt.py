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

    def do_seth(self, args):
        """Set tot hour in month event: Eg: seth 3, calculate tot hour in march and set it in a calendar event"""
        today = datetime.datetime.now
        if len(args) == 0:
            month = today.month - 1
        else:
            month = int(args)
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.set_totHoursEvent(month)

    def do_geth(self, args):
        """View tot hour in month. Eg: geth 3 returns March tot hours"""
        today = datetime.datetime.now
        if len(args) == 0:
            month = today.month - 1
        else:
            month = int(args)
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.get_totHoursEvent(month)

    def do_report(self, args):
        """Create time tracking pdf report"""
        today = datetime.datetime.now()
        locale.setlocale(locale.LC_TIME, "it")
        name = r"c:\temp\test_report_lab.pdf"
        argstuple = tuple(map(str, args.split()))
        if len(args) == 0:
            month = today.month - 1
            monthStr = calendar.month_name[month];
            mode = blm
            name = r"c:\mox\ivan.pernigo_" + monthStr + str(today.year) + ".pdf"
        elif len(args) == 1:
            month = int(args)
            monthStr = calendar.month_name[month];
            mode = blm
            name = r"c:\mox\ivan.pernigo_" + monthStr + str(today.year) + ".pdf"
        else:
            month = int(argstuple[0])
            monthStr = calendar.month_name[month];
            mode = argstuple[1]
            if mode == 'mox':
                name = r"c:\mox\MOXLab_ivan.pernigo_" + monthStr + str(today.year) + ".pdf"
            else:
                name = r"c:\mox\ivan.pernigo_" + monthStr + str(today.year) + ".pdf"

        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        events = evt.get_events(month=month)
        ret = evt.print_events(events, mode)
        print ('---------------')

        ### pdfWriter
        pdfw = pdfWriter.pdfWriter(name)
        pdfw.write_header('Consuntivo mensile Ivan Pernigo (Moxlab)')
        pdfw.write_header('Mese: ' + monthStr + ' ' + str(today.year))
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        if mode == 'blm':
            pdfw.write_header('Auto: propria = P ; non propria = NP', 'Normal')
        pdfw.write_header(' ')
        pdfw.write_header(' ')
        if mode == 'mox':
            ret['pevts'].insert(0,['G', 'Pres', 'Off', 'Trasferta', 'Auto', 'Pernotto'])
            ret['pevts'].append(['Tot', 'Ore', 'Off', '', '', ''])
            ret['pevts'].append(['', ret['totHours'], ret['permHours'], '', '', ''])
        else:
            ret['pevts'].insert(0,['G', 'Pres', 'Off', 'Trasferta', 'Auto', 'Pernotto', 'Entrata', 'Uscita', 'Entrata', 'Uscita'])
            ret['pevts'].append(['Tot', 'Ore', 'Off', '', '', '', '', '', '', ''])
            ret['pevts'].append(['', ret['totHours'], ret['permHours'], '', '', '', '', '', '', ''])
        pdfw.write_table(ret['pevts'])
        pdfw.build()

    def do_bill(self, args):
        """Create bill pdf"""
        today = datetime.datetime.now()
        locale.setlocale(locale.LC_TIME, "it")
        argstuple = tuple(map(str, args.split()))
        if len(args) == 0:
            month = today.month - 1
            year = str(today.year)
        elif len(args) == 1:
            month = int(args)
            year = str(today.year)
        else:
            month = int(argstuple[0])
            year = argstuple[1]

        num = month + 1
        name = r"c:\mox\\" + num + "_" + year + ".pdf"
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                    cfname='calendar-python-quickstart.json',
                    sfname='client_secret.json')

        ret = evt.get_data(month)
        totH = ret['totHours']
        totExp = ret['totExp']

        ### pdfWriter
        pdfw = pdfWriter.pdfWriter(name)
        pdfw.write_header('ing. Ivan Pernigo')
        pdfw.write_header('via Prà dei Prà, 22 - 37057,')
        pdfw.write_header('San Giovanni Lupatoto (VR)')
        pdfw.write_header('cell: 339-5012227')
        pdfw.write_header('e-mail: ipernigo@gmail.com')
        pdfw.write_header('codice fiscale: PRNVNI72T26L781T')
        pdfw.write_header('p.iva: 03829390230')
        pdfw.write_header('Verona, ' + today.strftime("%d/%m/%Y"))
        pdfw.write_header('Spett.le Mox Lab S.r.l.')
        pdfw.write_header('Via Marconi 22, Porto Valtravaglia (VA)')
        pdfw.write_header('P.I. 03498110125')
        pdfw.write_header('Fattura n.' + num + '/' + year + '			Onoranze')
        pdfw.write_header('______________________________________________________')

        costDay = 263
        costH = costDay / 8
        totCostH = costH*totH

        tab = [['Ore:','','', totH],
               ['Accordo contrattuale n. 1801', '', '', totCostH],
               ['Spese per trasferte', '','', totExp],
               ['Totale compensi', '', '', totCostH+totExp],
               []]

    def do_quit(self, args):
        """Quits TTT."""
        print ("Quitting.")
        raise SystemExit

if __name__ == '__main__':
    prompt = tttPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting TTT prompt...')
