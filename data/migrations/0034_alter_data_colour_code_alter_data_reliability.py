# Generated by Django 4.0.6 on 2022-08-18 10:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0033_alter_data_toplayer_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='colour_code',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='data',
            name='reliability',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]