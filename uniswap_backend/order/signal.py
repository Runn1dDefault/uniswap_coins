from django.utils.timezone import now, localtime
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import swap_task
from .models import Order


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:

        content = {
            'id': int(instance.id),
            'token_to': instance.token_to,
            'token_from': instance.token_from,
            'from_count': float(instance.from_count),
            'to_count': float(instance.to_count),
            'end_time': instance.end_time,
            'percentage': float(instance.percentage)
        }

        st_time = localtime(instance.start_time)

        if st_time <= localtime(now()):
            swap_task.delay(content=content)
        else:
            swap_task.apply_async(kwargs={'content': content}, eta=st_time)
