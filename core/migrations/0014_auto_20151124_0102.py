# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151115_0125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grow',
            options={'ordering': ['start_date'], 'permissions': (('view_grow', 'View grow'),)},
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='ec',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='lumen',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='tds',
        ),
        migrations.AddField(
            model_name='measurement',
            name='tds_ec',
            field=models.IntegerField(null=True, verbose_name=b'TDS/EC', blank=True),
        ),
        migrations.AlterField(
            model_name='grow',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='group',
            field=models.CharField(default=b'[Default Group]', max_length=35),
        ),
    ]
