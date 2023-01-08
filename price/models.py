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
    TYPE_CHOISES = (
        ('service', 'Услуга'),
        ('product', 'Товар'),
    )

    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='price_services', verbose_name='Прайс-лист')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, default=0.00)
    type = models.CharField(max_length=255, choices=TYPE_CHOISES, default='service', verbose_name='Тип услуги')
    code = models.CharField(max_length=63, verbose_name='Код')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.price}'


class DentalChart(models.Model):
    """Модель Зубная карта пациента"""
    client = models.OneToOneField(
        to='scheduler.Customer',
        on_delete=models.CASCADE,
        related_name='dental_chart')

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
    tooth_number = models.PositiveSmallIntegerField(verbose_name='Номер зуба', default=0)
    services = models.ManyToManyField(to=Service, blank=True, related_name='teeth')

    class Meta:
        verbose_name = 'Зуб'
        verbose_name_plural = 'Зубы'
