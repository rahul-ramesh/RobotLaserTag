# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0004_auto_20151118_0358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Angle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('team', models.IntegerField(default=1)),
                ('angle', models.IntegerField(default=0)),
            ],
        ),
    ]
