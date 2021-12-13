from order.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from order.tasks import celery_test


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:
        content = {
            'id': int(instance.id),
            'token_to': instance.token_to,
            'token_from': instance.token_from,
            'from_count': float(instance.from_count),
            'to_count': float(instance.to_count),
            'start_time': instance.start_time,
            'end_time': instance.end_time,
            'percentage': float(instance.percentage)
        }
        celery_test.delay(content=content)