# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-17 04:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bank_transactions', '0002_auto_20180216_2132'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial_transactions', '0001_initial'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalfinancialtransactionmatch',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfinancialtransactionmatch',
            name='transaction',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_transactions.FinancialTransaction'),
        ),
        migrations.AddField(
            model_name='historicalbankstatementmatch',
            name='attachment',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='documents.Attachment'),
        ),
        migrations.AddField(
            model_name='historicalbankstatementmatch',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbankstatementmatch',
            name='statement',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bank_transactions.Statement'),
        ),
        migrations.AddField(
            model_name='financialtransactionmatch',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Attachment'),
        ),
        migrations.AddField(
            model_name='financialtransactionmatch',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_transactions.FinancialTransaction'),
        ),
        migrations.AddField(
            model_name='bankstatementmatch',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Attachment'),
        ),
        migrations.AddField(
            model_name='bankstatementmatch',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_transactions.Statement'),
        ),
    ]