# Generated by Django 5.1 on 2024-09-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_restaurantcategory_rename_category_menuitemcategory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='image_url',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='menu_items/'),
        ),
        migrations.AlterModelTable(
            name='restaurantcategory',
            table='restaurants_restaurantcategory',
        ),
    ]
