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

    def get_token_to_price(self, token_input, token_output, quantity: int = 1):
        token_i = self.check_address(token_input)
        token_o = self.check_address(token_output)

        output = self.uniswap.get_price_input(
            token0=token_i.address,
            token1=token_o.address,
            qty=quantity * 10 ** token_i.decimals,
        )
        price = output / 10 ** token_o.decimals
        return price

    def make_trade(self, token_from, token_to, quantity: int = 1):
        token_input = self.check_address(token_from)
        token_output = self.check_address(token_to)

        x = self.uniswap.make_trade(
            token_input.address,
            token_output.address,
            quantity * 10 ** token_input.decimals
        )
        return x

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

    def make_trade(self):
        return self.uni_wrapper.make_trade(
            token_from=self.token_input,
            token_to=self.token_output,
            quantity=self.token_amount
        )
