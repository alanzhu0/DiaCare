# Generated by Django 3.2.15 on 2023-03-05 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20230305_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_clinic_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_food_received',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producechoice',
            name='category',
            field=models.CharField(choices=[('vegetables', 'Vegetables'), ('fruits', 'Fruits'), ('other', 'Other')], default='other', max_length=255),
        ),
    ]
