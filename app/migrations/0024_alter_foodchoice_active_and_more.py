# Generated by Django 4.1.7 on 2023-05-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0023_user_is_active_alter_user_admin_comments_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="foodchoice",
            name="active",
            field=models.BooleanField(
                default=True,
                help_text="Whether this food choice is currently available for selection",
            ),
        ),
        migrations.AlterField(
            model_name="producecategory",
            name="display_order",
            field=models.IntegerField(
                default=0,
                help_text="Order in which this category should be displayed to users",
            ),
        ),
        migrations.AlterField(
            model_name="producecategory",
            name="id",
            field=models.CharField(
                help_text="Unique identifier for this category",
                max_length=255,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="producechoice",
            name="active",
            field=models.BooleanField(
                default=True,
                help_text="Whether this produce choice is currently available for selection",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Whether the user is currently enrolled in the program and is authorized to log in and order food.",
                verbose_name="Active",
            ),
        ),
    ]