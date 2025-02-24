# Generated by Django 5.1.5 on 2025-01-26 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0004_relation_typo_fix'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalinvestment',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical investment', 'verbose_name_plural': 'historical investments'},
        ),
        migrations.AlterField(
            model_name='historicalinvestment',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
