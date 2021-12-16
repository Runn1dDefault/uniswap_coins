from django.utils.timezone import localtime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from uniswap_backend.celery import app
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
        task = swap_task.apply_async(kwargs={'content': content}, eta=st_time)
        instance.task_id = task.task_id
        instance.save()


@receiver(post_delete, sender=Order)
def pre_listing_request(sender, instance, **kwargs):
    print(instance.task_id, '---------------------------')
    app.control.revoke(str(instance.task_id), terminate=True)
