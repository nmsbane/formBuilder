# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-28 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_auto_20160528_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formcontents',
            name='input_type',
            field=models.CharField(max_length=50),
        ),
    ]
