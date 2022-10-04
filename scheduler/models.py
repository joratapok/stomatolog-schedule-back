from django.db import models
from timezone_field import TimeZoneField
from django.utils.timezone import now
from django.contrib.auth.models import User
from slugify import slugify


class StomatologyAbstractUser(models.Model):
    """ Абстрактная модель ползьователя"""
    stomatology_user_id = models.BigAutoField(primary_key=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения', db_index=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)

    class Meta:
        verbose_name = 'Пользователь стоматологии'
        verbose_name_plural = 'Пользователи стоматологии'
        ordering = ['-date_of_birth']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Employee(User, StomatologyAbstractUser):
    """Сотрудник клиники"""
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото сотрудника')
    speciality = models.CharField(max_length=255, verbose_name='Специальность')
    clinic = models.ManyToManyField(to='Clinic', related_name='employees', verbose_name='Клиника')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['speciality']


class Customer(StomatologyAbstractUser):
    """Модель клиента"""
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
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    gender = models.CharField(max_length=255, choices=GENDER, default='male', verbose_name='Пол')
    service = models.CharField(max_length=255, verbose_name='Услуга')
    status = models.CharField(max_length=255, choices=STATUS, default='not_confirmed')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Clinic(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование', unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)
    time_zone = TimeZoneField(default='Europe/Moscow')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Clinic, self).save(*args, **kwargs)


class Cabinet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Кабинет')
    clinic = models.ForeignKey(to=Clinic,
                               on_delete=models.CASCADE,
                               related_name='offices',
                               verbose_name='Клиника')

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        unique_together = ('name', 'clinic')

    def __str__(self):
        return f'{self.name}  ---  {self.clinic.title}'


class Event(models.Model):
    cabinet = models.ForeignKey(to=Cabinet,
                                on_delete=models.CASCADE,
                                related_name='cabinet_events',
                                verbose_name='Кабинет')

    dateStart = models.DateTimeField(default=now, verbose_name='Дата и время начала приема')
    dateFinish = models.DateTimeField(default=now, verbose_name='Дата и время окончания приема')

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
        return f'Врач: {self.doctor.__str__()}-' \
               f'{self.client.__str__()}-' \
               f'{self.dateStart.__str__()[:10]}-' \
               f'{self.cabinet.clinic.slug}'
