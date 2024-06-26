# Generated by Django 4.1.7 on 2023-07-06 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0056_delete_passwordresetlink"),
    ]

    operations = [
        migrations.CreateModel(
            name="PasswordResetLink",
            fields=[
                (
                    "emailverificationlink_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="app.emailverificationlink",
                    ),
                ),
            ],
            bases=("app.emailverificationlink",),
        ),
    ]
