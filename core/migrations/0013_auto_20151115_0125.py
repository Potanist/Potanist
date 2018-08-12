# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_measurement_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='label',
            new_name='group',
        ),
    ]
