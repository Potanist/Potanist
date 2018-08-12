# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20160225_0119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='reservoir_temperature',
        ),
        migrations.AddField(
            model_name='measurement',
            name='medium_temperature',
            field=models.FloatField(null=True, verbose_name=b'Reservoir / Soil Temperature', blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ph',
            field=models.FloatField(null=True, verbose_name=b'pH', blank=True),
        ),
    ]
