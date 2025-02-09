"""Migrations to add a submitter name to the transaction."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migrations for the FinancialTransaction model."""
    dependencies = [
        ('financial_transactions', '0006_alter_historicalfinancialcodematch_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialtransaction',
            name='submitter',
            field=models.CharField(
                blank=True,
                help_text='Individual who submitted or initiated this transaction',
                max_length=256,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='historicalfinancialtransaction',
            name='submitter',
            field=models.CharField(
                blank=True,
                help_text='Individual who submitted or initiated this transaction',
                max_length=256,
                null=True,
            ),
        ),
    ]
