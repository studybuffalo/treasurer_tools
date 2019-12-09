# Generated by Django 2.2.6 on 2019-11-09 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_institutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalaccount',
            name='institution',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The bank this account is associated with', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bank_institutions.Institution'),
        ),
    ]