from django.db import models
from timezone_field import TimeZoneField
from slugify import slugify
from django.contrib.auth.models import User
from employee.models import Profile
from price.models import PriceList, Service


class Customer(models.Model):
    """Модель клиента"""
    GENDER = (
        ('male', 'Mужчина'),
        ('female', 'Женщина'),
    )

    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения', db_index=True, auto_now=True)
    gender = models.CharField(max_length=255, choices=GENDER, default='male', verbose_name='Пол')
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True, default='8-999-888-77-66')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Clinic(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование', unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)
    time_zone = TimeZoneField(default='Europe/Moscow')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    start_of_the_day = models.CharField(max_length=10, default='08:00', verbose_name='Начало рабочего дня')
    end_of_the_day = models.CharField(max_length=10, default='17:00', verbose_name='Конец рабочего дня')
    is_main = models.BooleanField(default=False, verbose_name='Является главной')
    price_list = models.ForeignKey(PriceList,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True,
                                   related_name='clinic_services',
                                   verbose_name='Прайс-лист')

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'
        ordering = ['-is_main']

    def __str__(self):
        return f'{self.id} {self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Clinic, self).save(*args, **kwargs)


class Cabinet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Кабинет')
    clinic = models.ForeignKey(to=Clinic,
                               on_delete=models.CASCADE,
                               related_name='cabinets',
                               verbose_name='Клиника')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        unique_together = ('name', 'clinic')

    def __str__(self):
        return f'{self.name} --- {self.pk}'


class DutyShift(models.Model):
    date_start = models.DateTimeField(verbose_name='Дата и время начала дежурства')
    date_finish = models.DateTimeField(verbose_name='Дата и время окончания дежурства')
    doctor = models.ForeignKey(to=Profile,
                               on_delete=models.CASCADE,
                               related_name='duty_shift',
                               verbose_name='Доктор')

    cabinet = models.ForeignKey(to=Cabinet,
                                on_delete=models.CASCADE,
                                related_name='duty_shift_cabinet',
                                verbose_name='Кабинет')

    class Meta:
        verbose_name = 'Дежурство'
        verbose_name_plural = 'Дежурства'

    def __str__(self):
        return f'{self.doctor} {self.cabinet}'


class Event(models.Model):

    STATUS = (
        ('not_confirmed', 'Не подтвержден'),
        ('confirmed', 'Подтвержден'),
        ('reception_completed', 'Прием завершен'),
        ('canceled', 'Отменён'),
        ('no_show', 'Неявка'),
    )

    cabinet = models.ForeignKey(to=Cabinet,
                                on_delete=models.CASCADE,
                                related_name='cabinet_events',
                                verbose_name='Кабинет')

    date_start = models.DateTimeField(verbose_name='Дата и время начала приема')
    date_finish = models.DateTimeField(verbose_name='Дата и время окончания приема')
    services = models.ManyToManyField(to=Service, verbose_name='Услуги', related_name='service_events', blank=True)
    status = models.CharField(max_length=255, choices=STATUS, default='not_confirmed')
    color = models.CharField(max_length=255, verbose_name='Цвет', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    client = models.ForeignKey(to=Customer,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='customer_events',
                               verbose_name='Клиент')

    doctor = models.ForeignKey(to=Profile,
                               limit_choices_to={'role': 'doctor'},
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='doctor_events',
                               verbose_name='Лечащий врач')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'Врач: {self.doctor.__str__()}-' \
               f'{self.client.__str__()}-' \
               f'{self.date_start.__str__()[:10]}-' \
               f'{self.cabinet.clinic.slug}'
