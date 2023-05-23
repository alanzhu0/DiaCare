# Generated by Django 4.1.7 on 2023-05-22 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0033_user_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="dietician",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.dietician",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="doctor",
            field=models.ForeignKey(
                default=5, on_delete=django.db.models.deletion.CASCADE, to="app.doctor"
            ),
            preserve_default=False,
        ),
    ]
