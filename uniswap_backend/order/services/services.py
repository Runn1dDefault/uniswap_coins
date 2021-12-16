from order.services.instances import uniswap_instance
from order.convert import token_check_address


class UniSwapWrapper:

    def __init__(self, token_to, token_from, percentage, to_count, from_count, **kwargs):
        self.uniswap = uniswap_instance
        self.token_to = token_to
        self.token_from = token_from
        self.percentage = percentage
        self.price = to_count
        self.from_count = from_count
        self.token_from_address, self.from_decimal = token_check_address(token_from)
        self.token_to_address, self.to_decimal = token_check_address(token_to)

    def change_slippage(self, max_slippage: float):
        self.uniswap.default_slippage = max_slippage

    @property
    def get_token_to_price(self):
        output = self.uniswap.get_price_input(
            token0=self.token_from_address,
            token1=self.token_to_address,
            qty=self.get_quantity,
        )
        return output / 10 ** self.from_decimal

    def make_trade(self):
        return self.uniswap.make_trade(
            self.token_from_address, self.token_to_address, qty=self.get_quantity).hex()

    @property
    def max_slippage(self):
        return self.price * self.percentage / 100

    @property
    def max_and_min_price(self):
        max_price = self.price + self.max_slippage
        min_price = self.price - self.max_slippage
        return max_price, min_price

    @property
    def price_in_range(self):
        price = self.get_token_to_price
        max_price, min_price = self.max_and_min_price
        if min_price <= price <= max_price:
            return True
        return False

    @property
    def get_quantity(self):
        return int(self.from_count * 10 ** self.from_decimal)
