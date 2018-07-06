"""
Definition of models.
"""

from django.db import models
import datetime
import math

class DayTime(models.Model):
    """A day time object for use in the application views and repository."""
    day = models.DateField('date time', default=datetime.date.today, primary_key=True)
    totH = models.FloatField('day tot hour presence', default=0.0)
    offH = models.FloatField('day tot hour off', default=0.0)
    travel = models.CharField(max_length=50, blank=True)
    travel_cost = models.IntegerField('travel cost', default=0)
    overnigth_cost = models.IntegerField('overnigth cost', default=0)
    inM = models.TimeField('in:', default='00:00')
    outM = models.TimeField('out:', default='00:00')
    inA = models.TimeField('in:', default='00:00')
    outA = models.TimeField('out:', default='00:00')

    def calc_totH(self):
        """Calculates the day total hour presence."""
        now = datetime.datetime.now()
        hday = 0
        if self.outM.hour > 0 :
            inM = now.replace(hour=self.inM.hour, minute=self.inM.minute, second=0) 
            outM = now.replace(hour=self.outM.hour, minute=self.outM.minute, second=0) 
            span = outM - inM
            hday += span.total_seconds()
        if self.outA.hour > 0 :
            inA = now.replace(hour=self.inA.hour, minute=self.inA.minute, second=0) 
            outA = now.replace(hour=self.outA.hour, minute=self.outA.minute, second=0) 
            span = outA - inA
            hday += span.total_seconds()

        hh = hday/3600
        hm = math.floor(round(hh*4, 1))/4
        self.totH = hm
        return hm

    def total_hours(self):
        """Calculates the month total hour presence."""
        return self.choice_set.aggregate(Sum('totH'))['totHours']
    
    def total_hours(self):
        """Calculates the month total hour off."""
        return self.choice_set.aggregate(Sum('offH'))['totOffHours']

    def total_travCost(self):
        """Calculates the total travel cost."""
        return self.choice_set.aggregate(Sum('travel_cost'))['totTravCost']

    def total_overCost(self):
        """Calculates the total overnight cost."""
        return self.choice_set.aggregate(Sum('overnigth_cost'))['totOverCost']

    def __str__(self):
        return self.day.strftime("%d/%m/%Y") + ' - ' + str(self.totH) + ' h'
