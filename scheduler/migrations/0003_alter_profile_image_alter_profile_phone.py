# Generated by Django 4.1.1 on 2022-11-17 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото сотрудника'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=255, unique=True, verbose_name='Телефон'),
        ),
    ]
