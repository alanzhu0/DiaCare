# Generated by Django 4.1.7 on 2023-07-03 12:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0052_remove_user_next_clinic_visit_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="last_clinic_visit",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_food_received",
        ),
    ]
