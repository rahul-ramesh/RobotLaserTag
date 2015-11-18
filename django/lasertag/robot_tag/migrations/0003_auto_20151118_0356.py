# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0002_auto_20151116_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coords',
            name='x',
        ),
        migrations.RemoveField(
            model_name='coords',
            name='y',
        ),
    ]
