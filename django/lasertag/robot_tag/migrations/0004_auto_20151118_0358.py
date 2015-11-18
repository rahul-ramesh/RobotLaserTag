# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0003_auto_20151118_0356'),
    ]

    operations = [
        migrations.AddField(
            model_name='coords',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coords',
            name='y',
            field=models.IntegerField(default=0),
        ),
    ]
