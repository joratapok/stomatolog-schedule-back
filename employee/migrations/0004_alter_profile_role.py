# Generated by Django 4.1.1 on 2022-11-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_profile_role_alter_profile_speciality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('owner', 'Владелец'), ('administrator', 'Администратор'), ('doctor', 'Доктор')], default='doctor', max_length=255, verbose_name='Роль'),
        ),
    ]
