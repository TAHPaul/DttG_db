# Generated by Django 4.0.6 on 2022-08-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0023_alter_museum_museum_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='place_of_execution',
            field=models.ForeignKey(on_delete=models.SET('city was deleted'), related_name='execution_city', to='data.city'),
        ),
    ]
