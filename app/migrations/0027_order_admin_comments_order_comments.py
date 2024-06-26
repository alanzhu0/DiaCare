# Generated by Django 4.1.7 on 2023-05-21 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0026_remove_order_date_order_date_ordered"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="admin_comments",
            field=models.TextField(
                blank=True,
                help_text="Comments from food pharmacy staff regarding this order",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="comments",
            field=models.TextField(
                blank=True, help_text="Comments from the patient regarding this order"
            ),
        ),
    ]
