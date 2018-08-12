# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20160115_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='group',
            field=models.CharField(default=b'Ungrouped', max_length=35),
        ),
    ]
