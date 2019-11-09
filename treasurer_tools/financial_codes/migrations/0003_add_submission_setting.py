from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('financial_codes', '0002_add_short_name_to_budget_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialcodesystem',
            name='submission_code',
            field=models.BooleanField(default=False, help_text='Whether this code should be used for the financial code submission'),
        ),
        migrations.AddField(
            model_name='historicalfinancialcodesystem',
            name='submission_code',
            field=models.BooleanField(default=False, help_text='Whether this code should be used for the financial code submission'),
        ),
        migrations.AlterField(
            model_name='historicalbudgetyear',
            name='financial_code_system',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The financial code system that this budget year applies to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_codes.FinancialCodeSystem'),
        ),
        migrations.AlterField(
            model_name='historicalfinancialcodegroup',
            name='budget_year',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The budget year that this group applies to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='financial_codes.BudgetYear'),
        ),
    ]
