# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-09 05:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bank_transactions', '0002_auto_20180208_2203'),
        ('financial_transactions', '0002_auto_20180208_2203'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalReconciliationMatch',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bank_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bank_transactions.BankTransaction')),
                ('financial_transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_transactions.FinancialTransaction')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical reconciliation match',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='ReconciliationMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rm_bank_transaction', to='bank_transactions.BankTransaction')),
                ('financial_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rm_financial_transaction', to='financial_transactions.FinancialTransaction')),
            ],
        ),
    ]
