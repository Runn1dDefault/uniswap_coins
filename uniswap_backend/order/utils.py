import json
import re
from django.utils.timezone import now, localtime, timedelta

from uniswap_backend.celery import app


def time_edit(time_string: str):
    start_time = localtime(now())

    kwargs = dict()
    minutes = re.findall(r'\d+m', time_string)
    hours = re.findall(r'\d+h', time_string)
    days = re.findall(r'\d+d', time_string)
    seconds = re.findall(r'\d+s', time_string)

    if seconds:
        kwargs['seconds'] = int(seconds[0].replace('s', ''))
    if minutes:
        kwargs['minutes'] = int(minutes[0].replace('m', ''))
    if hours:
        kwargs['hours'] = int(hours[0].replace('h', ''))
    if days:
        kwargs['days'] = int(days[0].replace('d', ''))
    
    time_delta = start_time + timedelta(**kwargs)

    return start_time, time_delta


def check_task(task_id) -> bool:
    inspect = app.control.inspect()
    workers = inspect.active()
    if workers and workers.values():
        if task_id in workers.values():
            return True
    return False
