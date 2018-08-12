# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151222_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'permissions': (('view_photo', 'View photo'),)},
        ),
    ]
