# Generated by Django 4.1.7 on 2023-05-21 02:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0027_order_admin_comments_order_comments"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="comments",
            new_name="patient_comments",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="user_comments",
            new_name="patient_comments",
        ),
    ]
