# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151020_0132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='tag',
            new_name='label',
        ),
    ]
