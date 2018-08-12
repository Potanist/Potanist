# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151020_0152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='breeder',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='grow',
            options={'permissions': (('view_grow', 'View grow'),)},
        ),
        migrations.AlterModelOptions(
            name='strain',
            options={'ordering': ('name',)},
        ),
    ]
