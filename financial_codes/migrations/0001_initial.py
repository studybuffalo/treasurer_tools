# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-10 21:47
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
            name='BudgetYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(help_text='First day of the budget year')),
                ('date_end', models.DateField(help_text='Last day of the budget year')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='The numerical code for this financial code', max_length=6)),
                ('description', models.CharField(help_text='Description of this financial code', max_length=100)),
                ('budget_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financial_codes.BudgetYear')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCodeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code grouping', max_length=100)),
                ('description', models.CharField(help_text='Expanded description of the financial code gouping', max_length=500)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], help_text='Current status of this code system', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCodeSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code system', max_length=100)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], help_text='Current status of this code system', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalBudgetYear',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_start', models.DateField(help_text='First day of the budget year')),
                ('date_end', models.DateField(help_text='Last day of the budget year')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical budget year',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalFinancialCode',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('code', models.CharField(help_text='The numerical code for this financial code', max_length=6)),
                ('description', models.CharField(help_text='Description of this financial code', max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('budget_year', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_codes.BudgetYear')),
                ('code_group', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_codes.FinancialCodeGroup')),
                ('code_system', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_codes.FinancialCodeSystem')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical financial code',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalFinancialCodeGroup',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code grouping', max_length=100)),
                ('description', models.CharField(help_text='Expanded description of the financial code gouping', max_length=500)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], help_text='Current status of this code system', max_length=1)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical financial code group',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalFinancialCodeSystem',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code system', max_length=100)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], help_text='Current status of this code system', max_length=1)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical financial code system',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.AddField(
            model_name='financialcode',
            name='code_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financial_codes.FinancialCodeGroup'),
        ),
        migrations.AddField(
            model_name='financialcode',
            name='code_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_codes.FinancialCodeSystem'),
        ),
    ]
