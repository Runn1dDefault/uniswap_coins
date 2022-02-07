from django.utils.timezone import now
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from uniswap_backend.celery import app
from order.tasks import swap_task
from order.models import Order


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:
        task = swap_task.apply_async(kwargs={'order_id': instance.id}, eta=now())
        instance.task_id = task.task_id
        instance.status = 'Awaiting launch...'
        instance.save()


@receiver(post_delete, sender=Order)
def pre_listing_request(sender, instance, **kwargs):
    task_id = instance.task_id
    if task_id:
        try:
            app.control.revoke(task_id, terminate=True)
            print('Deleted task ID: {}'.format(instance.task_id))
        except Exception as e:
            print(e)
