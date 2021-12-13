from uniswap_backend.celery import app

from .models import Order
from .services.services import UniSwapWrapper, GasWrapper
from .services.instances import uniswap_instance


@app.task
def celery_test(content):
    uniswap = UniSwapWrapper(
            uniswap=uniswap_instance,
            gas_instance=GasWrapper(
                token_output_price=20,
                currency='usd'
            )
    )

    while True:
        price = uniswap.get_token_to_price(
            token_from=content.get('token_from'),
            token_to=content.get('token_to'),
            quantity=content.get('from_count')
        )

        count_per = content.get('to_count') * content.get('percentage') / 100

        plus_need_sum = content.get('to_count') + count_per
        minus_need_sum = content.get('to_count') - count_per

        print(minus_need_sum,'++++',  price, '++++', plus_need_sum)

        if minus_need_sum <= price <= plus_need_sum:
            # make trade
            uniswap.custom_make_trade(
                token_from=content.get('token_from'),
                token_to=content.get('token_to'),
                quantity=2
            )
            # Order save
            order = Order.objects.get(id=content.get('id'))
            order.status = True
            order.save()
            print('+++++++++')
            break
