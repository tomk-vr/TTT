"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
import datetime
from .forms import PostDayTime, PostDate
from .models import DayTime
import calendar
import locale
from .DBYearDate import DBYearDate
from .pdfWriter import pdfWriter
from django.db.models import Sum
import os

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.datetime.now().year,
        }
    )

def dtform(request):
    """Renders the day time form page."""
    assert isinstance(request, HttpRequest)
    qs = DayTime.objects.filter(day=datetime.datetime.now().strftime("%Y-%m-%d"))
    if qs.count() > 0:
        dt = qs[0]
    else:
        dt = DayTime()

    if request.method == "POST":
        form = PostDayTime(request.POST, instance=dt)
        if form.is_valid():
            if 'View' in form.data:
                day = request.POST.get('day')
                dt = DayTime.objects.get(day=day)
                form = PostDayTime(instance=dt)
            else:    
                post = form.save(commit=False)
                post.totH = post.calc_totH()
                off = 8 - post.totH
                if off > 0:
                    post.offH = off
                else:
                    post.offH = 0
                post.save()
    else:
        form = PostDayTime(instance=dt)
    
    return render(
        request,
        'app/dtform.html',
        {
            'title':'Time track',
            'year':datetime.datetime.now().year,
            'day':datetime.datetime.now().strftime("%d/%m/%Y"),
            'form':form,
            'daytime':dt,
        }
    )

def timesheet(request):
    """Renders the timesheet page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        print(request.POST)
        form = PostDate(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            
            qs = timesheetRequestHandler(date)

            day = datetime.datetime.now()
            if 'View' in form.data:
                day = date.replace(day=1)
            if 'Print' in form.data:
                day = date.replace(day=1)
                createPdf(date, qs)
            elif 'ViewDay' in form.data:
                day = request.POST.get('day')

            dt = qs.get(day=day.strftime("%Y-%m-%d"))
            dtform = PostDayTime(instance=dt) 

        else:
            return
    else:
        form = PostDate()
        form.date = datetime.date.today()
        date = form.date.replace(day=1)
        #print(date)
        qs = timesheetRequestHandler(date)
        
        dt = qs.get(day=datetime.datetime.now().strftime("%Y-%m-%d"))
        dtform = PostDayTime(instance=dt) 

    su = qs.aggregate(Sum('totH'), Sum('travel_cost'), Sum('overnigth_cost'))
    monthTotH = su['totH__sum']
    travCost = su['travel_cost__sum']
    overnCost = su['overnigth_cost__sum']


    return render(
        request,
        'app/timesheet.html',
        {
            'title':'Time sheet',
            'form':form,
            'queryset':qs,
            'monthTotH': monthTotH,
            'travCost' : travCost,
            'overnCost' : overnCost,
            'dtform' :dtform,
            'daytime':dt,
        }
    )

def timesheetRequestHandler(date):
    '''Create all year date empty'''
    if DayTime.objects.filter(day__gte=date).count() <= 0:
        # fillDB
        fdb = DBYearDate(scope='https://www.googleapis.com/auth/calendar',
                            cfname='calendar-python-quickstart.json',
                            sfname='client_secret.json')
        fdb.fillDB(date.year, True)

    lday = calendar.monthrange(date.year, date.month)[1]
    lastday = date.replace(day=lday) 
    qs = DayTime.objects.filter(day__gte=date).filter(day__lte=lastday)
    return qs            


def createPdf(date, qs):
    
    locale.setlocale(locale.LC_TIME, "it")
    monthStr = calendar.month_name[date.month];
    month = date.month - 1
    if month == 12:
        year = str(date.year -1)
    else:
        year = str(date.year)
    reppath = r"C:\Users\ivan.pernigo.BLMGROUP\Google Drive\Ing.IvanPernigo - amministrazione\fatture vendita\\" + str(year) + "\\" + str(date.month+1) + "_" + str(year) + "\\";
    if not os.path.exists(reppath):
        os.makedirs(reppath)
    name = reppath + r"MOXLab_ivan.pernigo_" + monthStr + str(date.year) + ".pdf"
    res = []
    resblm = []
    totexp = 0
    totovc = 0;
    totH = 0.0
    offH = 0.0
    for q in qs:
        totexp += q.travel_cost
        totovc += q.overnigth_cost
        totH += q.totH
        offH += q.offH
        hh = ''
        if q.totH > 0.0:
            hh = str(q.totH)
        off = ''
        if q.offH > 0:
            off = str(q.offH)
        exp = ''
        if q.travel_cost > 0:
            exp = str(q.travel_cost)
        ovcost = ''
        if q.overnigth_cost > 0:
            ovcost = str(q.overnigth_cost)
        res.append([q.day.day, hh, off, q.travel, exp, ovcost])
        inM = ''
        outM = ''
        inA = ''
        outA = ''
        if q.inM.hour > 0:
            inM = q.inM.strftime("%H:%M")
        if q.outM.hour > 0:
            outM = q.outM.strftime("%H:%M")
        if q.inA.hour > 0:
            inA = q.inA.strftime("%H:%M")
        if q.outA.hour > 0:
            outA = q.outA.strftime("%H:%M")
        
        if 'sosta' not in q.travel:
            if q.travel_cost >= 120:
                exp = 'P'
            elif q.travel_cost > 0:
                exp = 'NP'

        resblm.append([q.day.day, hh, off, q.travel, exp, ovcost, inM, outM, inA, outA])

    res.insert(0, ['G', 'Pres', 'Off', 'Trasferta', 'Auto', 'Pernotto'])
    res.append(['Tot', 'Ore', 'Off', '', '', ''])
    res.append(['', totH, offH, '', totexp, totovc])
    
    ### pdfWriter
    pdfw = pdfWriter(name)
    pdfw.write_header('Consuntivo mensile Ivan Pernigo (Moxlab)')
    pdfw.write_header('Mese: ' + monthStr + ' ' + str(date.year))
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_table(res)
    pdfw.build()

    name = reppath + r"ivan.pernigo_" + monthStr + str(date.year) + ".pdf"
    
    ### pdfWriter
    pdfw = pdfWriter(name)
    pdfw.write_header('Consuntivo mensile Ivan Pernigo (Moxlab)')
    pdfw.write_header('Mese: ' + monthStr + ' ' + str(date.year))
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    pdfw.write_header('Auto: propria = P ; non propria = NP', 'Normal')
    pdfw.write_header(' ')
    pdfw.write_header(' ')
    resblm.insert(0,['G', 'Pres', 'Off', 'Trasferta', 'Auto', 'Pernotto', 'Entrata', 'Uscita', 'Entrata', 'Uscita'])
    resblm.append(['Tot', 'Ore', 'Off', '', '', '', '', '', '', ''])
    resblm.append(['', totH, offH, '', totexp, totovc, '', '', '', ''])
    pdfw.write_table(resblm)
    pdfw.build()

    billo(date, qs, '')
    billo (date, qs, 'mb')

def billo(date, qs, mb):
    locale.setlocale(locale.LC_TIME, "it")
    if date.month == 12:
        year = str(date.year + 1)
        num = "1" 
    else:
        year = str(date.year)
        num = str(date.month + 1)

    reppath = r"C:\Users\ivan.pernigo.BLMGROUP\Google Drive\Ing.IvanPernigo - amministrazione\fatture vendita\\" + year + "\\" + num + "_" + year + "\\";
    name = reppath + num + "_" + year + ".pdf"
    mbargs = mb

    totExp = 0
    totH = 0.0
    for q in qs:
        totExp += q.travel_cost + q.overnigth_cost
        totH += q.totH

    today = datetime.datetime.now();
    ### pdfWriter
    pdfw = pdfWriter(name)
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
    #impIVA = totPay + in4perc
    #iva = impIVA*22/100 
    totBill = totPay + in4perc
    #rit20per = -totPay*20/100
    tab = [['Fattura n.' + num + '/' + year,'','Ore', 'Onoranze'],
            ['Accordo contrattuale n. 1801', '', totH, "%.2f" % (totCostH)],
            ['Spese per trasferte', '','', "%.2f" % (totExp)],
            ['Totale compensi', '', '', "%.2f" % (totPay)],
            ['Contributo integrativo Inarcassa  4%', '', '', "%.2f" % (in4perc)],
            #['Imponibile Iva', '', '', "%.2f" % (impIVA)],
            #['Iva 22%', '', '', "%.2f" % (iva)],
            ['Totale fattura','','', "%.2f" % (totBill)],
            #['Ritenuta irpef 20% su totale compensi', '', '', "%.2f" % (rit20per)],
            #['Netto da pagare', '', '', "%.2f" % (totBill+rit20per)]
            ]

    pdfw.write_table(tab, False)
    pdfw.write_header('')
    pdfw.write_header('')
    pdfw.write_header('')
    pdfw.write_header('Operazione senza applicazione dell\'IVA ai sensi dell\'art.1, comma 58, Legge n.190/2014', 'Normal', alignment='l')
    pdfw.write_header('')
    pdfw.write_header('Operazione senza applicazione della ritenuta alla fonte a titolo di acconto ai sensi dell\'art.1, comma 67, Legge n.190/2014', 'Normal', alignment='l')
    pdfw.write_header('')
    pdfw.write_header('')
    pdfw.write_header('Termine di pagamento: 30gg. d.f.f.m.', 'Normal', alignment='l')
    pdfw.write_header('L’importo della presente fattura potrà anche essere pagato mediante bonifico bancario sul c/c n. 000005348814 intestato a Ivan Pernigo c/o Unicredit Banca, agenzia Verona Scuderlando ABI 02008 CAB 11727 CIN “P” – IBAN IT 25 P 02008 11727 000005348814.', 'Normal', alignment='l')

    if mbargs == "mb":
        pdfw.write_header('')
        pdfw.write_header('')
        pdfw.write_header('Marca da bollo assolta sull\'originale', 'Normal', alignment='l')
        nname = reppath + "__" + num + "_" + year + ".pdf"
        os.rename(name, nname)
       
    pdfw.build()