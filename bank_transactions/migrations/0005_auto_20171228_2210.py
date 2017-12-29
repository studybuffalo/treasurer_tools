# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-29 05:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_transactions', '0004_auto_20171228_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='institution',
            field=models.ForeignKey(help_text='The bank this account is associated with', on_delete=django.db.models.deletion.CASCADE, to='bank_transactions.Institution'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='account',
            field=models.ForeignKey(help_text='The account this statement belong to', on_delete=django.db.models.deletion.PROTECT, to='bank_transactions.Account'),
        ),
    ]
