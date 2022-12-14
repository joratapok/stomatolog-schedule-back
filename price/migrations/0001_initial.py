# Generated by Django 4.1.1 on 2022-12-22 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Прайс-лист')),
            ],
            options={
                'verbose_name': 'Прайс-лист',
                'verbose_name_plural': 'Прайс-листы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Цена')),
                ('type', models.CharField(choices=[('service', 'Услуга'), ('product', 'Товар')], default='service', max_length=255, verbose_name='Тип услуги')),
                ('code', models.CharField(max_length=63, verbose_name='Код')),
                ('price_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_services', to='price.pricelist', verbose_name='Прайс-лист')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['title'],
            },
        ),
    ]
