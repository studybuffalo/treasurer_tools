# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-14 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_historicalitem_historicaltransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The pre-tax dollar value', max_digits=12),
        ),
        migrations.AlterField(
            model_name='historicalitem',
            name='gst',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The tax (GST/HST) dollar value', max_digits=12),
        ),
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The pre-tax dollar value', max_digits=12),
        ),
        migrations.AlterField(
            model_name='item',
            name='gst',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The tax (GST/HST) dollar value', max_digits=12),
        ),
    ]