from django.utils.timezone import localtime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from uniswap_backend.celery import app
from .tasks import swap_task
from .models import Order

# TODO: Throttling the number of running processes
<<<<<<< HEAD
=======
from .utils import check_task
>>>>>>> cc5c87c... frontend changes


@receiver(post_save, sender=Order)
def pre_listing_request(sender, instance, created, **kwargs):
    if created:
<<<<<<< HEAD
        content = {
            'id': int(instance.id),
            'token_to': instance.token_to,
            'token_from': instance.token_from,
            'count_from': float(instance.count_from),
            'count_to': float(instance.count_to),
            'end_time': instance.end_time,
            'percentage': float(instance.percentage)
        }
        st_time = localtime(instance.start_time)
        task = swap_task.apply_async(kwargs={'content': content}, eta=st_time)
        instance.task_id = task.task_id
=======
        st_time = localtime(instance.start_time)
        task = swap_task.apply_async(kwargs={'order_id': instance.id}, eta=st_time)
        instance.task_id = task.task_id
        instance.status = Order.StatusChoices.WAIT
>>>>>>> cc5c87c... frontend changes
        instance.save()


@receiver(post_delete, sender=Order)
def pre_listing_request(sender, instance, **kwargs):
<<<<<<< HEAD
    print('Deleted task ID: {}'.format(instance.task_id))
    app.control.revoke(str(instance.task_id), terminate=True)
=======
    task_id = instance.task_id

    if task_id and check_task(task_id):
        print('Deleted task ID: {}'.format(instance.task_id))
        app.control.revoke(task_id, terminate=True)
>>>>>>> cc5c87c... frontend changes
