# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151112_0343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='water_temperature',
            new_name='reservoir_temperature',
        ),
    ]
