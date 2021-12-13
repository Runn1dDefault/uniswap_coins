import os
from celery import Celery
# from settings import BROKER_TRANSPORT_OPTIONS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniswap_backend.settings')

app = Celery('uniswap_backend')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
