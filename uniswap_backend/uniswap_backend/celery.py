import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniswap_backend.settings')

app = Celery('uniswap_backend')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'execute_tokens_every_three_hours': {
        'schedule': crontab(minute=0, hour='*/3'),
        'task': 'order.tasks.tokens_save'
    }
}

