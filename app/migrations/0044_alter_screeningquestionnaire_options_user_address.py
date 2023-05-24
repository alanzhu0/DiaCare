# Generated by Django 4.1.7 on 2023-05-24 00:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0043_screeningquestionnaire_date_completed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="screeningquestionnaire",
            options={"ordering": ["-date_completed"]},
        ),
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=512),
        ),
    ]