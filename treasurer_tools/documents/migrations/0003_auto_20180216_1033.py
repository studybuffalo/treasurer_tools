# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-16 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_bankstatementmatch_historicalbankstatementmatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='location',
            field=models.FileField(max_length='255', upload_to='attachments'),
        ),
    ]