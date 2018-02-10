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
            name='BudgetYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(help_text='First day of the budget year', verbose_name='start date')),
                ('date_end', models.DateField(help_text='Last day of the budget year', verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='The numerical code for this financial code', max_length=6)),
                ('description', models.CharField(help_text='Description of this financial code', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCodeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code grouping', max_length=100)),
                ('description', models.CharField(help_text='Expanded description of the financial code gouping', max_length=500)),
                ('type', models.CharField(choices=[('e', 'Expense'), ('r', 'Revenue')], default='e', max_length=1)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], default='a', help_text='Current status of this code system', max_length=1)),
                ('budget_year', models.ForeignKey(help_text='The budget year that this group applies to', on_delete=django.db.models.deletion.PROTECT, to='financial_codes.BudgetYear')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCodeSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the financial code system', max_length=100)),
                ('date_start', models.DateField(help_text='First day this assignment applies to', verbose_name='start date')),
                ('date_end', models.DateField(blank=True, help_text='Last day this assignment applies to (leave blank for no end date)', null=True, verbose_name='end date')),
            ],
        ),
        migrations.AddField(
            model_name='financialcode',
            name='financial_code_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financial_codes.FinancialCodeGroup'),
        ),
        migrations.AddField(
            model_name='budgetyear',
            name='financial_code_system',
            field=models.ForeignKey(help_text='The financial code system that this budget year applies to', on_delete=django.db.models.deletion.PROTECT, to='financial_codes.FinancialCodeSystem'),
        ),
    ]
