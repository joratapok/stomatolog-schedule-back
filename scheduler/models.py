from django.db import models
import datetime
from timezone_field import TimeZoneField
# from django.contrib.auth.models import User


class StomatologyUser(models.Model):
    """ Абстрактная модель ползьователя"""
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения', db_index=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)

    class Meta:
        verbose_name = 'Пользователь стоматологии'
        verbose_name_plural = 'Пользователи стоматологии'
        ordering = ['-date_of_birth']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Employee(StomatologyUser):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото сотрудника')
    speciality = models.CharField(max_length=255, verbose_name='Специальность')
    clinic = models.ManyToManyField(to='Clinic', related_name='employees', verbose_name='Клиника')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['speciality']


class Customer(StomatologyUser):
    GENDER = (
        ('male', 'Mужчина'),
        ('female', 'Женщина'),
    )
    STATUS = (
        ('not_confirmed', 'Не подтвержден'),
        ('confirmed', 'Подтвержден'),
        ('reception_completed', 'Прием завершен'),
        ('Canceled', 'Отменён'),
        ('no_show', 'Неявка'),
    )
    gender = models.CharField(max_length=255, choices=GENDER, default='male', verbose_name='Пол')
    duration_of_admission = models.TimeField(default=datetime.time(00, 15), verbose_name='Длительность приема')
    service = models.CharField(max_length=255, verbose_name='Услуга')
    status = models.CharField(max_length=255, choices=STATUS, default='not_confirmed')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Clinic(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)
    time_zone = TimeZoneField(default='Europe/Moscow')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'

    def __str__(self):
        return self.title


class Cabinet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Кабинет')
    clinic = models.ForeignKey(to=Clinic, on_delete=models.CASCADE, related_name='offices', verbose_name='Клиника')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return self.name


class Event(models.Model):
    cabinet = models.ForeignKey(to=Cabinet,
                                on_delete=models.CASCADE,
                                related_name='cabinet_events',
                                verbose_name='Кабинет')
    date = models.DateField(verbose_name='Дата приема')

    time = models.TimeField(default=datetime.time(8, 00), verbose_name='Длительность приема')
    client = models.ForeignKey(to=Customer,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='customer_events',
                               verbose_name='Клиент')

    doctor = models.ForeignKey(to=Employee,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='employee_events',
                               verbose_name='Лечащий врач')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'Врач: {self.doctor.__str__()} - Посетитель: {self.client.__str__()}'
