# Generated by Django 4.0.6 on 2022-08-02 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_alter_museum_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='rkd_link',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]
