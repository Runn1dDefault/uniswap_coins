from celery.schedules import crontab

from django.utils.timezone import now, localtime
from django.db.models.signals import post_save
from django.dispatch import receiver

from uniswap_backend.celery import app

from .tasks import celery_test
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

        st_time = instance.start_time

        if st_time <= localtime(now()):
            celery_test.delay(content=content)
        else:
            start_time = instance.start_time

            app.add_periodic_task(
                crontab(
                    hour=start_time.hour,
                    minute=start_time.minute,
                    day_of_month=start_time.day,
                    month_of_year=start_time.month
                ),
                celery_test.s(content=content),
                name=f'OrderID: {kwargs.get("id")}'
            )
