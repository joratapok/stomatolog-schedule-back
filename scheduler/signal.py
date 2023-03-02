from django.db.models.signals import post_save
from django.dispatch import receiver
from scheduler.models import Customer
from price.models import DentalChart


@receiver(post_save, sender=Customer)
def create_customer_dental_chart(sender, instance, created, **kwargs):
    if created:
        DentalChart.objects.create(client=instance)
