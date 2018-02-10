# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-10 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2)),
                ('country_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='PayeePayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The individual, company, or organization name', max_length=250, unique=True)),
                ('address', models.CharField(help_text='The Mailing address for this individual', max_length=1000)),
                ('city', models.CharField(max_length=1000)),
                ('province', models.CharField(help_text='Mailing address province, state, etc.', max_length=100)),
                ('postal_code', models.CharField(blank=True, help_text='Mailing address postal code, zip code, etc.', max_length=10, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='phone number')),
                ('fax', models.CharField(blank=True, max_length=30, null=True, verbose_name='fax number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(choices=[('a', 'active'), ('i', 'inactive')], help_text='Whether this individual has recent expense or revenue activity', max_length=2)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payee_payers.Country')),
            ],
            options={
                'verbose_name_plural': 'Payee/Payers',
            },
        ),
    ]
