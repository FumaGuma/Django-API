# Generated by Django 5.0.1 on 2024-01-11 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admissions", "0005_remove_user_is_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="approved",
            field=models.BooleanField(default=False),
        ),
    ]