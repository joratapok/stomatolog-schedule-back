from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE = (
        ('owner', 'Владелец'),
        ('administrator', 'Администратор'),
        ('doctor', 'Доктор'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество')
    role = models.CharField(max_length=255, choices=ROLE, default='doctor', verbose_name='Роль')
    date_of_birth = models.DateField(verbose_name='Дата рождения', db_index=True, auto_now_add=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', unique=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото сотрудника', null=True, blank=True)
    speciality = models.CharField(max_length=255, verbose_name='Специальность', null=True, blank=True)
    clinic = models.ManyToManyField('scheduler.Clinic', related_name='profiles', verbose_name='Клиники')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.is_superuser:
                Profile.objects.create(user=instance, phone='1')
            else:
                Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()