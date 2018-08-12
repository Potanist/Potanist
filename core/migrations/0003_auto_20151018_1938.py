# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151015_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grow',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
