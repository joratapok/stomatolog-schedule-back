from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_user_admin_fields(sender, instance, created, **kwargs):
    if created:
        if User.objects.count() == 1:
            User.objects.filter(id=instance.id).update(last_name='admin', first_name='admin')
