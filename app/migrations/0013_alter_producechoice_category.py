# Generated by Django 3.2.15 on 2023-03-05 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20230305_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producechoice',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producecategory'),
        ),
    ]
