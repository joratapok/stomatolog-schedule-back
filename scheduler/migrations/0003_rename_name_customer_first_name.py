# Generated by Django 4.1.1 on 2022-09-26 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_customer_duration_of_admission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='first_name',
        ),
    ]