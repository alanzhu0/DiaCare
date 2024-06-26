# Generated by Django 4.1.7 on 2023-05-23 00:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0035_alter_user_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="Whether the user is currently enrolled in the Food Pharmacy program and is authorized to log in and order food.",
                verbose_name="Active",
            ),
        ),
    ]
