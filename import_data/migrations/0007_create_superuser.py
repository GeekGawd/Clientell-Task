import os
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('import_data', '0006_alter_opportunity_account_alter_opportunity_user'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin'
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]