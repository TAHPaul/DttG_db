# Generated by Django 4.0.6 on 2022-08-02 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='artist2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_artist', to='data.artist'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='id',
            field=models.CharField(help_text='Please use the following formatting: M###', max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='museum_link',
            field=models.URLField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='rkd_link',
            field=models.URLField(blank=True, unique=True),
        ),
    ]
