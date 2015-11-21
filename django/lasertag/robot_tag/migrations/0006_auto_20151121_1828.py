# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_tag', '0005_angle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('team', models.IntegerField(default=1)),
                ('command', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='fault',
            name='victim',
        ),
        migrations.AddField(
            model_name='map',
            name='x',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='map',
            name='y',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='fault',
            name='attacker',
            field=models.CharField(default=b'1', max_length=10),
        ),
        migrations.AlterField(
            model_name='map',
            name='map',
            field=models.CharField(max_length=10000),
        ),
    ]
