# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payee_payers', '0002_auto_20180216_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpayeepayer',
            name='city',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='payeepayer',
            name='city',
            field=models.CharField(max_length=250),
        ),
    ]
