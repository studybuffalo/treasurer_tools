# Generated by Django 2.0.3 on 2018-09-30 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_codes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetyear',
            name='short_name',
            field=models.CharField(default='ADD SHORT NAME', help_text='A short name to identify the budget year', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalbudgetyear',
            name='short_name',
            field=models.CharField(default='ADD SHORT NAME', help_text='A short name to identify the budget year', max_length=16),
            preserve_default=False,
        ),
    ]