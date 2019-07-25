"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import DayTime
import datetime
from .MonthYearWidget import MonthYearWidget

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class PostDayTime(forms.ModelForm):

    class Meta:
        model = DayTime
        fields = ('day', 'inM', 'outM', 'inA', 'outA', 'travel', 'travel_cost', 'overnigth_cost')
        widgets = {
            'day': forms.DateInput(attrs={'class': 'day', 'size': 7}, format='%Y-%m-%d'),
            'inM': forms.TimeInput(attrs={'class': 'inM', 'size': 7}, format='%H:%M'),
            'outM': forms.TimeInput(attrs={'class': 'outM', 'size': 7}, format='%H:%M'),
            'inA': forms.TimeInput(attrs={'class': 'inA', 'size': 7}, format='%H:%M'),
            'outA': forms.TimeInput(attrs={'class': 'outA', 'size': 7}, format='%H:%M'),
            'travel' : forms.TextInput(attrs={'size': 7}),
            'travel_cost' : forms.TextInput(attrs={'size': 7}),
            'overnigth_cost' : forms.TextInput(attrs={'size': 7}),
        }

class PostDate(forms.Form):
    date = forms.DateField(
        initial=datetime.date.today,
        required=False,
        widget=MonthYearWidget(years=range(2017,2035)),
    )