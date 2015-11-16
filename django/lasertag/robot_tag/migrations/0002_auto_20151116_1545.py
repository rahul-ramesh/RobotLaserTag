# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='map',
            field=models.CharField(max_length=100),
        ),
    ]
