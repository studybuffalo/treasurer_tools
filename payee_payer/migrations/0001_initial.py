# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-03 20:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Demographics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The individual, company, or organization name', max_length=256)),
                ('address', models.CharField(help_text='The Mailing address for this individual', max_length=1000)),
                ('city', models.CharField(max_length=1000)),
                ('province', models.CharField(help_text='Mailing address province, state, etc.', max_length=100)),
                ('postal_code', models.CharField(help_text='Mailing address postal code, zip code, etc.', max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('a', 'active'), ('i', 'inactive')], help_text='Whether this individual has current activity expenses or revenue', max_length=2)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payee_payer.Country')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Demographics',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDemographics',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(help_text='The individual, company, or organization name', max_length=256)),
                ('address', models.CharField(help_text='The Mailing address for this individual', max_length=1000)),
                ('city', models.CharField(max_length=1000)),
                ('province', models.CharField(help_text='Mailing address province, state, etc.', max_length=100)),
                ('postal_code', models.CharField(help_text='Mailing address postal code, zip code, etc.', max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('a', 'active'), ('i', 'inactive')], help_text='Whether this individual has current activity expenses or revenue', max_length=2)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('country', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payee_payer.Country')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical demographics',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
