# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_measurement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='ppm',
        ),
        migrations.AlterField(
            model_name='measurement',
            name='air_temperature',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='co2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ec',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='humidity',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ph',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='water_temperature',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
