from django.utils import timezone
from uniswap_backend.celery import app

from order.models import Order
from order.services.services import UniSwapWrapper

import time


@app.task
def swap_task(order_id):
    order = Order.objects.get(id=order_id)
    order.status = Order.StatusChoices.PROCESS
    order.save()

    swap_wrapper = UniSwapWrapper(order)
    try:
        # loop for check price
        while timezone.now() <= order.end_time:
            if swap_wrapper.trader_checker():
                break
            else:
                print('-------------------------')
            # rate limit of request to avoid connection errors
            time.sleep(10)

        if order.contract_address == '' and timezone.now() >= order.end_time:
            order.status = Order.StatusChoices.OVERWTRADE
            order.save()

    except Exception as e:
        print(e)
        order.status = Order.StatusChoices.FAILED
        order.save()
