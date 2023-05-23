# Generated by Django 4.1.7 on 2023-05-21 17:19

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("address", "0003_auto_20200830_1851"),
        ("app", "0032_delete_feed_remove_user_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=address.models.AddressField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="address.address",
            ),
        ),
    ]