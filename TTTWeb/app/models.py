"""
Definition of models.
"""

from django.db import models
import datetime

class DayTime(models.Model):
    """A day time object for use in the application views and repository."""
    day = models.DateField('date time', default=datetime.date.today)
    totH = models.FloatField('day tot hour presence', default=0.0)
    offH = models.FloatField('day tot hour off', default=0.0)
    travel = models.CharField(max_length=50)
    travel_cost = models.IntegerField('business travel cost', default=0)
    overnigth_cost = models.IntegerField('business travel overnigth cost', default=0)
    inM = models.TimeField('morning entry time')
    outM = models.TimeField('morning exit time')
    inA = models.TimeField('afternoon entry time')
    outA = models.TimeField('afternoon exit time')

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