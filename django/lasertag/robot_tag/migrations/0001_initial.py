# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('team', models.IntegerField(default=1)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fault_type', models.IntegerField(default=1)),
                ('victim', models.IntegerField(default=1)),
                ('attacker', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('map', models.CommaSeparatedIntegerField(max_length=100)),
            ],
        ),
    ]
