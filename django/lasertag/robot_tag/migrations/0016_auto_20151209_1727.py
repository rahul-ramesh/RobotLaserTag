# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-09 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0015_auto_20151209_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='when',
            field=models.IntegerField(default=1),
        ),
    ]