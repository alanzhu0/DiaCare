# Generated by Django 4.1.7 on 2023-07-03 12:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0051_alter_securelink_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="next_clinic_visit",
        ),
        migrations.RemoveField(
            model_name="user",
            name="next_food_batch",
        ),
    ]