# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-14 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180627_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytime',
            name='hol',
            field=models.BooleanField(default=False, verbose_name='hol:'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='inA',
            field=models.TimeField(default='00:00', verbose_name='in:'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='inM',
            field=models.TimeField(default='00:00', verbose_name='in:'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='outA',
            field=models.TimeField(default='00:00', verbose_name='out:'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='outM',
            field=models.TimeField(default='00:00', verbose_name='out:'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='overnigth_cost',
            field=models.IntegerField(default=0, verbose_name='overnigth cost'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='travel',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='travel_cost',
            field=models.IntegerField(default=0, verbose_name='travel cost'),
        ),
    ]