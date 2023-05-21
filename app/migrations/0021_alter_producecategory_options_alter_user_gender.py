# Generated by Django 4.1.7 on 2023-05-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0020_auto_20230305_0557"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="producecategory",
            options={
                "ordering": ["display_order", "name"],
                "verbose_name_plural": "Produce categories",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("male", "Male"),
                    ("female", "Female"),
                    ("nonbinary", "Non-binary"),
                ],
                max_length=255,
            ),
        ),
    ]