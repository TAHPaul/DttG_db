# Generated by Django 4.0.6 on 2022-08-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0020_alter_artist_image_alter_artwork_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='museum',
            field=models.ForeignKey(on_delete=models.SET('museum was deleted'), related_name='artwork_museum', to='data.museum'),
        ),
    ]