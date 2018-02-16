# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_institutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(blank=True, help_text='The account number/reference for this account', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaccount',
            name='account_number',
            field=models.CharField(blank=True, help_text='The account number/reference for this account', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='fax',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='fax number'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='fax',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='fax number'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number'),
        ),
    ]