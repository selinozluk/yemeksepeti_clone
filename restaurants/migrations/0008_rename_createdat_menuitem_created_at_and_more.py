# Generated by Django 5.1 on 2024-10-03 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_alter_menuitem_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='menuitem',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='updatedAt',
            new_name='updated_at',
        ),
    ]
