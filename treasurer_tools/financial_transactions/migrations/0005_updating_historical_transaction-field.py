from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('financial_transactions', '0004_add_submission_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalfinancialtransaction',
            name='payee_payer',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The individual, organization, or company this transaction applies to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payee_payers.PayeePayer', verbose_name='payee or payer'),
        ),
    ]
