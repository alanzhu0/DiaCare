# Generated by Django 4.1.7 on 2023-05-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0046_user_email_verified_emailverificationlink"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dietician",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
