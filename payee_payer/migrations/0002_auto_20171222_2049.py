# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-23 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payee_payer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='fax',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Fax number'),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Mailing address postal code, zip code, etc.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='status',
            field=models.CharField(choices=[('a', 'active'), ('i', 'inactive')], help_text='Whether this individual has recent expense or revenue activity', max_length=2),
        ),
        migrations.AlterField(
            model_name='historicaldemographics',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldemographics',
            name='fax',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Fax number'),
        ),
        migrations.AlterField(
            model_name='historicaldemographics',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='historicaldemographics',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Mailing address postal code, zip code, etc.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldemographics',
            name='status',
            field=models.CharField(choices=[('a', 'active'), ('i', 'inactive')], help_text='Whether this individual has recent expense or revenue activity', max_length=2),
        ),
    ]