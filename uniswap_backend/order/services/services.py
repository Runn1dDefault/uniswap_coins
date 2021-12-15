from django.conf import settings
from typing import Union

from uniswap.token import ERC20Token
from web3 import Web3, middleware
from uniswap import Uniswap

from .instances import get_web3_instance, uniswap_instance
from web3.gas_strategies.time_based import fast_gas_price_strategy


class UniSwapWrapper:

    def __init__(self, uniswap: Uniswap):
        self.uniswap = uniswap

    def change_slippage(self, max_slippage: float):
        self.uniswap.default_slippage = max_slippage

    def get_token_to_price(self, token_input, token_output, quantity: Union[float, int] = 0.01):
        token_input_address = self.check_address(
            token_input).address if token_input != settings.BASE_TOKEN_ADDRESS else token_input
        token_output_address = self.check_address(
            token_output).address if token_output != settings.BASE_TOKEN_ADDRESS else token_output

        output = self.uniswap.get_price_input(
            token0=token_input_address,
            token1=token_output_address,
            qty=int(quantity * 10 ** self.get_token_decimal(token_output)),
        )
        price = output / 10 ** self.get_token_decimal(token_input)
        return price

    def make_trade(self, token_from, token_to, quantity: Union[float, int] = 0.01):
        token_input_address = self.check_address(
            token_from).address if token_from != settings.BASE_TOKEN_ADDRESS else token_from
        token_output_address = self.check_address(
            token_to).address if token_to != settings.BASE_TOKEN_ADDRESS else token_to

        x = self.uniswap.make_trade(
            token_input_address,
            token_output_address,
            int(quantity * 10 ** self.get_token_decimal(token_from))
        )
        return x.hex()

    def get_token_decimal(self, token_address):
        if token_address == settings.BASE_TOKEN_ADDRESS:
            return 18
        return self.check_address(token_address).decimals

    def check_address(self, token) -> ERC20Token:
        token_address = Web3.toChecksumAddress(token)
        return self.uniswap.get_token(token_address)

    def change_gas_strategy(self):
        w3 = get_web3_instance()

        if not w3.isConnected():
            raise ConnectionError('Invalid http provider')

        w3.eth.set_gas_price_strategy(fast_gas_price_strategy)
        w3.middleware_onion.add(middleware.time_based_cache_middleware)
        w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        w3.middleware_onion.add(middleware.simple_cache_middleware)

        self.uniswap.w3 = w3


class SwapWrapper:
    def __init__(self, token_to, token_from, percentage, to_count, from_count):
        self.uni_wrapper = UniSwapWrapper(uniswap=uniswap_instance)

        self.token_output = token_to
        self.token_input = token_from
        self.percentage = percentage
        self.price = to_count
        self.token_amount = from_count

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
        price = self.uni_wrapper.get_token_to_price(
            token_input=self.token_input,
            token_output=self.token_output,
            quantity=self.token_amount
        )

        max_price, min_price = self.max_and_min_price

        if min_price <= price <= max_price:
            return True
        return False

    @property
    def eth_balance(self):
        """
            For get token balance:
                self.uni_wrapper.uniswap.get_token_balance(valid_token_address)
        """
        return self.uni_wrapper.uniswap.get_eth_balance()

    def make_trade_custom(self):

        return self.uni_wrapper.make_trade(
            token_from=self.token_input,
            token_to=self.token_output,
            quantity=self.token_amount
        )
