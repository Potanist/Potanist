# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_grow_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('air_temperature', models.IntegerField(null=True, blank=True)),
                ('water_temperature', models.IntegerField(null=True, blank=True)),
                ('humidity', models.IntegerField(null=True, blank=True)),
                ('co2', models.IntegerField(null=True, blank=True)),
                ('ppm', models.IntegerField(null=True, blank=True)),
                ('tds', models.IntegerField(null=True, blank=True)),
                ('ec', models.IntegerField(null=True, blank=True)),
                ('ph', models.IntegerField(null=True, blank=True)),
                ('lumen', models.IntegerField(null=True, blank=True)),
                ('plant', models.ForeignKey(to='core.Plant')),
            ],
        ),
    ]
