# Generated by Django 5.1 on 2024-10-03 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastName',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
