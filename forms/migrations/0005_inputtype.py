# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-28 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_formresults'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
        ),
    ]
