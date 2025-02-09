"""Updated plural verbose name of Branch model."""
from django.db import migrations


class Migration(migrations.Migration):
    """Updates to the Branch model."""
    dependencies = [
        ('branch_details', '0002_alter_historicalbranch_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='historicalbranch',
            options={
                'get_latest_by': ('history_date', 'history_id'),
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical Branch',
                'verbose_name_plural': 'historical Branches',
            },
        ),
    ]
