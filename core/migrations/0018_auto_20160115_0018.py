# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20151222_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='grow',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='grow',
            name='end_date',
            field=models.DateField(help_text=b'To mark a grow as complete, specify an end date.', null=True, blank=True),
        ),
    ]
