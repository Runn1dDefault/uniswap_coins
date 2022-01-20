import time

import requests
from decimal import Decimal
from statistics import mean

from order.models import OrderPrice, Order
from order.services.instances import get_uniswap_instance


class UniSwapWrapper:
    def __init__(self, order, **kwargs):
        self.kwargs = kwargs
        self.order = order
        self.uniswap = get_uniswap_instance()

        self.token_from = self.uniswap.w3.toChecksumAddress(self.order.token_from.address)
        self.from_decimals = self.order.token_from.decimals

        self.token_to = self.uniswap.w3.toChecksumAddress(self.order.token_to.address)
        self.to_decimals = self.order.token_to.decimals

    @property
    def get_token_to_price(self):
        output = self.uniswap.get_price_input(
            token0=self.token_from,
            token1=self.token_to,
            qty=self.get_quantity,
        )
        return output / 10 ** self.from_decimals

    @property
    def max_slippage(self):
        return (self.order.count_to * self.order.percentage) / 100

    @property
    def max_and_min_price(self) -> tuple:
        max_price = self.order.count_to + self.max_slippage
        min_price = self.order.count_to - self.max_slippage
        return max_price, min_price

    def get_min_now_price(self, price: Decimal):
        if price > 0:
            return price + (price * self.order.percentage) / 100
        return 0

    def get_max_now_price(self, price: Decimal):
        return price - (price * self.order.percentage) / 100

    def trader_checker(self) -> bool:
        prices = []
        max_sleep, min_sleep = self.max_and_min_price
        is_traded = False

        while len(prices) != 3:
            price = self.get_price()
            if price:
                prices.append(price)
                if not is_traded and min_sleep <= price <= max_sleep:
                    contract_address = self.make_trade()  # do make trade
                    self.order.save_contact(contract_address)
                    is_traded = True
            time.sleep(10)

        max_price, min_price, mean_price = max(prices), min(prices), mean(prices)
        prices.remove(max_price)
        prices.remove(min_price)
        price = prices[0]

        OrderPrice.objects.create(
            order=self.order, price=price,
            mean_price=mean_price,
            max_price=max_price,
            min_price=min_price
        )
        return is_traded

    @property
    def get_quantity(self) -> int:
        return int(self.order.count_from * 10 ** self.from_decimals)

    def get_price(self):
        url = f'https://api.uniswap.org/v1/quote?' \
              f'protocols=v2,v3&' \
              f'tokenInAddress={self.token_from}' \
              f'&tokenInChainId={self.order.token_from.chainId}' \
              f'&tokenOutAddress={self.token_to}' \
              f'&tokenOutChainId={self.order.token_to.chainId}' \
              f'&amount={self.get_quantity}&type=exactIn'

        response = requests.get(url, headers={'origin': 'https://app.uniswap.org'})
        if response.status_code == 200:
            return Decimal(response.json()['quoteDecimals'])

    def make_trade(self):
        return self.uniswap.make_trade(self.token_from, self.token_to, qty=self.get_quantity).hex()
