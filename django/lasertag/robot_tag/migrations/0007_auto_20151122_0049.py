# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0006_auto_20151121_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='angle',
            name='name',
        ),
        migrations.RemoveField(
            model_name='command',
            name='name',
        ),
        migrations.RemoveField(
            model_name='coords',
            name='name',
        ),
        migrations.AlterField(
            model_name='fault',
            name='attacker',
            field=models.IntegerField(default=1),
        ),
    ]
