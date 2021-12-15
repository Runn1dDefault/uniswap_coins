from datetime import datetime

from django.conf import settings
from django.utils.timezone import now, localtime, utc

from uniswap_backend.celery import app

from .models import Order
from .services.services import SwapWrapper


@app.task
def swap_task(content):
    end_time = localtime(
        datetime.strptime(
            content.pop('end_time'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).astimezone(tz=utc if settings.USE_TZ else None)
    )
    order_id = content.pop('id')
    # this class for swap logic construct
    print(content)

    swap_wrapper = SwapWrapper(
        **content
    )

    while localtime(now()) <= end_time:
        if swap_wrapper.price_in_range:
            # do make trade
            contract_address = swap_wrapper.make_trade_custom()

            print(contract_address)
            # Order status update
            Order.find_and_status_update(contract_address, id=order_id)

            break
        else:
            print('-------------------------')
