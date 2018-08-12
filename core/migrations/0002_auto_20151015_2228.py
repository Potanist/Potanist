# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='core.Group')),
                ('grow', models.ForeignKey(to='core.Grow')),
            ],
        ),
        migrations.RemoveField(
            model_name='plant',
            name='group',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='grow',
        ),
        migrations.AddField(
            model_name='grow',
            name='groups',
            field=models.ManyToManyField(to='core.Group', through='core.GrowGroup'),
        ),
        migrations.AddField(
            model_name='plant',
            name='growgroup',
            field=models.ForeignKey(default=None, to='core.GrowGroup'),
            preserve_default=False,
        ),
    ]
