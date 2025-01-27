# Generated by Django 5.1.5 on 2025-01-26 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payee_payers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalpayeepayer',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical payee payer', 'verbose_name_plural': 'historical Payee/Payers'},
        ),
        migrations.AlterField(
            model_name='historicalpayeepayer',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
