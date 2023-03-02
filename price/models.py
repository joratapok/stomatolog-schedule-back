from django.core.validators import MaxValueValidator
from django.db import models


class PriceList(models.Model):
    """Модель Прайс-листа"""
    title = models.CharField(max_length=255, verbose_name='Прайс-лист')

    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Service(models.Model):
    """Модель Услуга"""
    TYPE_CHOICES = (
        ('service', 'Услуга'),
        ('product', 'Товар'),
    )

    price_list = models.ForeignKey(
        PriceList, on_delete=models.CASCADE, related_name='price_services', verbose_name='Прайс-лист'
    )
    title = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, default=0.00)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='service', verbose_name='Тип услуги')
    code = models.CharField(max_length=63, verbose_name='Код')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.price}'


class DentalChart(models.Model):
    """Модель Зубная карта пациента"""
    client = models.OneToOneField(to='scheduler.Customer', on_delete=models.CASCADE, related_name='dental_chart')

    class Meta:
        verbose_name = 'Зубная карта'
        verbose_name_plural = 'Зубные карты'

    def __str__(self):
        return self.client.__str__()


class Teeth(models.Model):
    """Модель Зубы"""
    dental_chart = models.ForeignKey(
        to=DentalChart,
        on_delete=models.CASCADE,
        related_name='teeth',
        verbose_name='Зубная карта')
    tooth_number = models.PositiveSmallIntegerField(
        verbose_name='Номер зуба', default=0, validators=[MaxValueValidator(63)])
    dental_services = models.ManyToManyField(to=Service, blank=True, related_name='teeth', verbose_name='Услуги')
    count = models.PositiveSmallIntegerField(verbose_name='Количество', default=1)
    event = models.ForeignKey(
        to='scheduler.Event',
        on_delete=models.SET_NULL,
        verbose_name='Событие',
        blank=True,
        null=True,
        related_name='services'
    )

    class Meta:
        verbose_name = 'Зуб'
        verbose_name_plural = 'Зубы'

    def __str__(self):
        return f'{self.dental_chart.client.__str__()} {self.tooth_number}'
