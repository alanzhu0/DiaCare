# Generated by Django 4.1.7 on 2023-05-20 18:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0021_alter_producecategory_options_alter_user_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="admin_comments",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="user",
            name="medical_comments",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="user",
            name="user_comments",
            field=models.TextField(blank=True),
        ),
    ]