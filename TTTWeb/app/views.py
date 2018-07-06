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
            post = form.save(commit=False)
            post.totH = post.calc_totH()
            post.save()
    else:
        form = PostDayTime(instance=dt)
    
    return render(
        request,
        'app/dtform.html',
        {
            'title':'Day time form',
            'year':datetime.datetime.now().year,
            'day':datetime.datetime.now().strftime("%d/%m/%Y"),
            'form':form,
            'daytime':dt
        }
    )

def timesheet(request):
    """Renders the timesheet page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = PostDate(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            lday = calendar.monthrange(date.year, date.month)[1]
            lastday = date.replace(day=lday) 
            qs = DayTime.objects.filter(day__gte=date).filter(day__lte=lastday)
    else:
        form = PostDate()
        form.date = datetime.date.today()
        qs = DayTime.objects.none()
    
    return render(
        request,
        'app/timesheet.html',
        {
            'title':'Timesheet',
            'form':form,
            'queryset':qs,
        }
    )

