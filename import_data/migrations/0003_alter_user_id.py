# Generated by Django 4.0.6 on 2022-07-09 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_data', '0002_alter_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]