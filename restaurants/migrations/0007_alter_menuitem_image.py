# Generated by Django 5.1 on 2024-09-16 10:01

import restaurants.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_remove_menuitem_image_url_menuitem_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=restaurants.models.upload_to),
        ),
    ]
