# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0010_auto_20151123_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='team',
            field=models.CharField(default=1, max_length=20),
        ),
    ]
