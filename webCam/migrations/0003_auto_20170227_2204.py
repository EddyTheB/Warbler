# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webCam', '0002_remove_computer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computer',
            name='computerID',
        ),
        migrations.AddField(
            model_name='computer',
            name='type',
            field=models.CharField(default='unknown', max_length=28),
            preserve_default=False,
        ),
    ]
