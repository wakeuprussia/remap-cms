# Generated by Django 4.0.4 on 2022-04-19 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_location_lat_location_lon'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttranslation',
            name='old_md',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
