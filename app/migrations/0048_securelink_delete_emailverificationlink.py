# Generated by Django 4.1.7 on 2023-05-24 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0047_alter_dietician_email_alter_doctor_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="SecureLink",
            fields=[
                (
                    "token",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("valid", models.BooleanField(default=True)),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="EmailVerificationLink",
        ),
    ]