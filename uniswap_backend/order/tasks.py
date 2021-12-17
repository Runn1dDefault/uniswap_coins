from django.utils import timezone
from django.utils.dateparse import parse_datetime

from uniswap_backend.celery import app

from order.models import Order
from order.services.services import UniSwapWrapper

import time


@app.task
def swap_task(content):
    swap_wrapper = UniSwapWrapper(**content)
    while timezone.now() <= parse_datetime(content.get('end_time')):
        time.sleep(5)
        if swap_wrapper.price_in_range:
            # do make trade
            contract_address = swap_wrapper.make_trade()
            Order.find_and_status_update(contract_address, id=content.get('id'))
            break
        else:
            print('-------------------------')
