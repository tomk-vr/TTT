"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import PostDayTime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
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
            'year':datetime.now().year,
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
            'year':datetime.now().year,
        }
    )

def dtform(request):
    """Renders the day time form page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        model = PostDayTime(request.POST)
        if model.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        model = PostDayTime()
    
    return render(
        request,
        'app/dtform.html',
        {
            'title':'Day time form',
            'year':datetime.now().year,
            'now':datetime.now().strftime("%H:%M"),
            'day':datetime.now().strftime("%d/%m/%Y"),
            'model': model,
        }
    )

