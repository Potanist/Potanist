# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breeder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('group_type', models.CharField(max_length=10, choices=[(b'Room', b'Room'), (b'Reservoir', b'Reservoir')])),
            ],
        ),
        migrations.CreateModel(
            name='Grow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('methodology', models.CharField(max_length=12, choices=[(b'Soil', b'Soil'), (b'Hydroponics', b'Hydroponics')])),
                ('breeder', models.ForeignKey(to='core.Breeder')),
                ('group', models.ForeignKey(to='core.Group')),
                ('grow', models.ForeignKey(to='core.Grow')),
            ],
        ),
        migrations.CreateModel(
            name='PlantStage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('stage', models.CharField(max_length=12, choices=[(b'Seed', b'Seed'), (b'Seedling', b'Seedling'), (b'Vegetative', b'Vegetative'), (b'Flowering', b'Flowering'), (b'Flush', b'Flush'), (b'Drying', b'Drying'), (b'Curing', b'Curing')])),
                ('date', models.DateTimeField()),
                ('plant', models.ForeignKey(to='core.Plant')),
            ],
        ),
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('strain_type', models.CharField(max_length=10, choices=[(b'Sativa', b'Sativa'), (b'Indica', b'Indica'), (b'Hybrid', b'Hybrid'), (b'Ruderalis', b'Ruderalis')])),
                ('flowering_time', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('breeder', models.ForeignKey(to='core.Breeder')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='strain',
            field=models.ForeignKey(to='core.Strain'),
        ),
    ]
