# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-30 18:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_auto_20160528_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formcontents',
            name='values',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.FormValues'),
        ),
    ]
