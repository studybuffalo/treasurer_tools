# Generated by Django 2.0.3 on 2018-07-08 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payee_payers', '0004_auto_20180708_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payeepayer',
            options={'ordering': ['name'], 'verbose_name_plural': 'Payee/Payers'},
        ),
    ]
