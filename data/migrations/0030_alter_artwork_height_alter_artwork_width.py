# Generated by Django 4.0.6 on 2022-08-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0029_alter_artist_year_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='width',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
