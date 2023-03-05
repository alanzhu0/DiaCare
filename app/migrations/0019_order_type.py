# Generated by Django 3.2.15 on 2023-03-05 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_order_date_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], default='pickup', max_length=255),
        ),
    ]
