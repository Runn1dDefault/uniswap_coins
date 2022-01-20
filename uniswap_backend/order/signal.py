from django.utils.timezone import localtime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from uniswap_backend.celery import app
from .tasks import swap_task
from .models import Order

from .utils import check_task
# TODO: Throttling the number of running processes


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:
        st_time = localtime(instance.start_time)
        task = swap_task.apply_async(kwargs={'order_id': instance.id}, eta=st_time)
        instance.task_id = task.task_id
        instance.status = Order.StatusChoices.WAIT
        instance.save()


@receiver(post_delete, sender=Order)
def pre_listing_request(sender, instance, **kwargs):
    task_id = instance.task_id

    if task_id and check_task(task_id):
        print('Deleted task ID: {}'.format(instance.task_id))
        app.control.revoke(task_id, terminate=True)
