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

    def do_in(self, args):
        """Set time of entry. Eg: in -1 set as time of entry datetime.now - 1 minutes"""
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                                cfname='calendar-python-quickstart.json',
                                sfname='client_secret.json')
        evt.set_in(int(args), "")

    def do_inf(self, args):
        """Set time of entry. Eg: inf 05/06/2018 08:13 set time of entry for June 05"""
        argstuple = tuple(map(str, args.split()))
        if len(argstuple) == 2:
            descr = ""
        elif len(argstuple) == 4:
            descr = "'Trasferta':'{}', 'Spese':'{}', 'Pernotto':'{}'".format(argstuple[2], argstuple[3], 0)
            descr = "{" + descr + "}"
        elif len(argstuple) == 5:
            descr = "'Trasferta':'{}', 'Spese':'{}', 'Pernotto':'{}'".format(argstuple[2], argstuple[3], argstuple[4])
            descr = "{" + descr + "}"
        else:
            print("Invalid args")
            return

        day = data = datetime.datetime.strptime(argstuple[0] + " " + argstuple[1], "%d/%m/%Y %H:%M")
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.set_in(0, descr, day)

    def do_out(self, args):
        """Set exit time. Eg: out -1 set as exit datetime.now - 1 minutes"""
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                                cfname='calendar-python-quickstart.json',
                                sfname='client_secret.json')
        evt.set_out(int(args))

    def do_outf(self, args):
        """Set exit time. Eg: outf 05/06/2018 13:07 set exit time for June 05"""
        argstuple = tuple(map(str, args.split()))
        if len(argstuple) < 2:
            print("Invalid args")
            return

        day = data = datetime.datetime.strptime(argstuple[0] + " " + argstuple[1], "%d/%m/%Y %H:%M")
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.set_out(0, day)

    def do_print(self, args):
        """Print time tracking of given month. Eg: print 3 return march time track"""
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                                cfname='calendar-python-quickstart.json',
                                sfname='client_secret.json')
        events = evt.get_events(month=int(args))
        evt.print_events(events)

    def do_import(self, args):
        """Import time track from csv timesheet e create related calendar events. Eg: import 'c:\march.csv'"""
        imp = importCsv.ImportCsv()
        imp.importData(args)

    def do_seth(self, args):
        """Set tot hour in month event.
        Eg: seth 3, calculate tot hour in march and set it in a calendar event
            seth 3 2018 167.75, set tot hour in march to value 167.75"""
        today = datetime.datetime.now()
        argstuple = tuple(map(str, args.split()))
        if len(argstuple) == 0:
            month = today.month - 1
            year = today.year
            forcedVal = 0
        elif len(argstuple) == 1:
            month = int(args)
            year = today.year
            forcedVal = 0
        elif len(argstuple) == 2:
            month = int(argstuple[0])
            year = int(argstuple[1])
            forcedVal = 0
        elif len(argstuple) == 3:
            month = int(argstuple[0])
            year = int(argstuple[1])
            forcedVal = argstuple[2]

        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                        cfname='calendar-python-quickstart.json',
                        sfname='client_secret.json')
        evt.set_totHoursEvent(month, year, forcedVal)

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
        evt.get_totHours(month)

    def do_report(self, args):
        """Create time tracking pdf report. Eg: report 3 mox"""
        today = datetime.datetime.now()
        locale.setlocale(locale.LC_TIME, "it")
        name = r"c:\temp\test_report_lab.pdf"
        argstuple = tuple(map(str, args.split()))
        if len(argstuple) == 0:
            month = today.month - 1
            monthStr = calendar.month_name[month];
            mode = blm
            name = r"c:\mox\ivan.pernigo_" + monthStr + str(today.year) + ".pdf"
        elif len(argstuple) == 1:
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
        """Create bill pdf. Eg: bill 3"""
        today = datetime.datetime.now()
        locale.setlocale(locale.LC_TIME, "it")
        argstuple = tuple(map(str, args.split()))
        if len(argstuple) == 0:
            month = today.month - 1
            year = str(today.year)
        elif len(argstuple) == 1:
            month = int(args)
            year = str(today.year)
        else:
            month = int(argstuple[0])
            year = argstuple[1]

        num = month + 1
        name = r"c:\mox\\" + str(num) + "_" + year + ".pdf"
        evt = tttEvent.TTTEvent(scope='https://www.googleapis.com/auth/calendar',
                    cfname='calendar-python-quickstart.json',
                    sfname='client_secret.json')

        events = evt.get_events(month=month)
        ret = evt.get_data(events, 'mox')
        totHevt = evt.get_totHoursEvents(month, year, events)
        totH = float(totHevt['description'])
        totExp = ret['totExp']

        ### pdfWriter
        pdfw = pdfWriter.pdfWriter(name)
        pdfw.write_header('ing. Ivan Pernigo', 'Heading2', alignment='c')
        pdfw.write_header('via Prà dei Prà, 22 - 37057,', 'Heading4', alignment='c')
        pdfw.write_header('San Giovanni Lupatoto (VR)', 'Heading4', alignment='c')
        pdfw.write_header('cell: 339-5012227', 'Heading4', alignment='c')
        pdfw.write_header('e-mail: ipernigo@gmail.com', 'Heading4', alignment='c')
        pdfw.write_header('codice fiscale: PRNVNI72T26L781T', 'Heading4', alignment='c')
        pdfw.write_header('p.iva: 03829390230', 'Heading4', alignment='c')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('Verona, ' + today.strftime("%d/%m/%Y"), 'Normal', alignment='r')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('Spett.le Mox Lab S.r.l.', 'Normal', alignment='l')
        pdfw.write_header('Via Marconi 22, Porto Valtravaglia (VA)', 'Normal', alignment='l')
        pdfw.write_header('P.I. 03498110125', 'Normal', alignment='l')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')

        costDay = 263
        costH = costDay / 8
        totCostH = costH*totH
        totPay = totCostH+totExp
        in4perc = (totCostH+totExp)*4/100
        impIVA = totPay + in4perc
        iva = impIVA*22/100 
        totBill = impIVA + iva
        rit20per = -totPay*20/100
        tab = [['Fattura n.' + str(num) + '/' + year,'','Ore', 'Onoranze'],
               ['Accordo contrattuale n. 1801', '', totH, "%.2f" % (totCostH)],
               ['Spese per trasferte', '','', "%.2f" % (totExp)],
               ['Totale compensi', '', '', "%.2f" % (totPay)],
               ['Contributo integrativo Inarcassa  4%', '', '', "%.2f" % (in4perc)],
               ['Imponibile Iva', '', '', "%.2f" % (impIVA)],
               ['Iva 22%', '', '', "%.2f" % (iva)],
               ['Totale fattura','','', "%.2f" % (totBill)],
               ['Ritenuta irpef 20% su totale compensi', '', '', "%.2f" % (rit20per)],
               ['Netto da pagare', '', '', "%.2f" % (totBill+rit20per)]]

        pdfw.write_table(tab, False)
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('Termine di pagamento: 30gg. d.f.f.m.', 'Normal', alignment='l')
        pdfw.write_header('L’importo della presente fattura potrà anche essere pagato mediante bonifico bancario sul c/c n. 000005348814 intestato a Ivan Pernigo c/o Unicredit Banca, agenzia Verona Scuderlando ABI 02008 CAB 11727 CIN “P” – IBAN IT 25 P 02008 11727 000005348814.', 'Normal', alignment='l')
        pdfw.build()
        print("Tot. fattura: %.2f" % (totBill+rit20per) + ' €')

    def do_quit(self, args):
        """Quits TTT."""
        print ("Quitting.")
        raise SystemExit

if __name__ == '__main__':
    prompt = tttPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting TTT prompt...')
