# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 12:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180624_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytime',
            name='day',
            field=models.DateField(default=datetime.date.today, verbose_name='date time'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='offH',
            field=models.FloatField(default=0.0, verbose_name='day tot hour off'),
        ),
        migrations.AlterField(
            model_name='daytime',
            name='totH',
            field=models.FloatField(default=0.0, verbose_name='day tot hour presence'),
        ),
    ]
