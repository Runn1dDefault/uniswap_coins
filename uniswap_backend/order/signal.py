from order.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from order.tasks import celery_test


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:
        content = {
            'token_to': instance.token_to,
            'token_from': instance.token_from,
            'from_count': instance.from_count,
            'to_count': instance.to_count
        }
        celery_test.delay(content=content)