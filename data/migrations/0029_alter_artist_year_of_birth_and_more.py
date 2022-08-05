# Generated by Django 4.0.6 on 2022-08-05 07:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0028_alter_artist_place_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='year_of_birth',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2022)]),
        ),
        migrations.AlterField(
            model_name='artist',
            name='year_of_death',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2022)]),
        ),
    ]
