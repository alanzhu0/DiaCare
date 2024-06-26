# Generated by Django 4.1.7 on 2023-05-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0024_alter_foodchoice_active_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-date_scheduled"]},
        ),
        migrations.RemoveField(
            model_name="order",
            name="complete",
        ),
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="date ordered"),
        ),
    ]
