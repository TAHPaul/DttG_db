# Generated by Django 4.0.6 on 2022-08-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0030_alter_artwork_height_alter_artwork_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='embargo',
            field=models.BooleanField(default=False),
        ),
    ]
