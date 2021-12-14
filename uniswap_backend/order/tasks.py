from django.utils.timezone import now

from uniswap_backend.celery import app

from .models import Order
from .services.services import SwapWrapper


@app.task
def celery_test(content):
    end_time = content.pop('end_time')
    # this class for swap logic construct
    swap_wrapper = SwapWrapper(
        **content
    )

    while now() <= end_time:
        if swap_wrapper.price_in_range:
            # do make trade
            swap_wrapper.make_trade()
            # Order status update
            Order.find_and_status_update(id=content.get('id'))

            # TODO: need revoke this task after successfully ended
            break
