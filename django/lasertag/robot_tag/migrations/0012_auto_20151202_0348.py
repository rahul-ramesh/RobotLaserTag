# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-02 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0011_auto_20151123_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fault',
            old_name='fault_type',
            new_name='power',
        ),
        migrations.AddField(
            model_name='fault',
            name='wheel',
            field=models.IntegerField(default=1),
        ),
    ]
