# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151124_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to=b'', verbose_name=b'Image')),
                ('taken_timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Taken At')),
                ('grow', models.ForeignKey(to='core.Grow', null=True)),
                ('plant', models.ForeignKey(to='core.Plant', null=True)),
            ],
        ),
    ]
