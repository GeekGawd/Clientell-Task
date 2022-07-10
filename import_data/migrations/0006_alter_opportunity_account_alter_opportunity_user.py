# Generated by Django 4.0.6 on 2022-07-10 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('import_data', '0005_alter_opportunity_account_alter_opportunity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='import_data.account'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='import_data.user'),
        ),
    ]