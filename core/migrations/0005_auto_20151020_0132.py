# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_plant_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='growgroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='growgroup',
            name='grow',
        ),
        migrations.RemoveField(
            model_name='grow',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='breeder',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='growgroup',
        ),
        migrations.AddField(
            model_name='plant',
            name='grow',
            field=models.ForeignKey(to='core.Grow'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='tag',
            field=models.CharField(default=b'(Unlabeled)', max_length=35),
        ),
        migrations.AlterField(
            model_name='plantstage',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GrowGroup',
        ),
    ]
