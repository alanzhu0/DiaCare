# Generated by Django 4.1.7 on 2023-05-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0029_order_number_alter_order_admin_comments_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="producecategory",
            options={
                "ordering": ["display_order", "name"],
                "verbose_name_plural": "produce categories",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="cancelled",
            field=models.BooleanField(
                default=False, help_text="Whether this order was cancelled"
            ),
        ),
    ]
