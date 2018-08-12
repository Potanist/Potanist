# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151114_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
