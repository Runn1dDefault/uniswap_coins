from pprint import pprint

from uniswap_backend.celery import app

from order.models import Order, Coin
from order.services.services import trade_loop_run


@app.task
def swap_task(order_id):
    order = Order.objects.get(id=order_id)
    try:
        order.status = 'In process'
        order.save()
        trade_loop_run(order)
        order.status = 'Stopped'
        order.save()
    except Exception as e:
        if 'Insufficient balance.' in str(e):
            order.status = 'Insufficient balance.'
        else:
            order.status = 'Failed'
        order.save()
        pprint(e)


@app.task
def tokens_save():
    pprint('Tokens update...')
    # It's only for a mainnet network
    Coin.get_all_tokens_and_save()
