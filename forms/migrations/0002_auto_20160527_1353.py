# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-27 13:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formcontents',
            name='values',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forms.FormValues'),
        ),
    ]
