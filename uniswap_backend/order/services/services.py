import time
from typing import Union

import requests
from web3 import Web3
from uniswap import Uniswap

from .decorators import multiprocess, auto_change_version
from .instances import GAS_ENDPOINT, PROVIDER


class GasWrapper:
    # hierarchy is respected
    prices_names = ('slow', 'normal', 'fast', 'instant')
    price_currency = ('gwei', 'usd')

    def __init__(self, max_gas_price: float, currency: str):
        self.prices_count = len(self.prices_names)
        self.max_gas_price = max_gas_price
        self.currency = currency.strip().lower()
        self._check_currency()

    def _check_currency(self):
        if self.currency not in self.price_currency:
            raise ValueError(f'Currency must be in {self.price_currency}')

    @multiprocess
    def gas_price_selection(self):
        gas_json = self.gas_info()

        for name in list(reversed(self.prices_names)):

            price = gas_json.get(name).get(self.currency)

            if price < self.max_gas_price:
                return price

        return gas_json.get('normal').get(self.currency)

    @multiprocess
    def gas_max_price(self):
        gas_json = self.gas_info()
        return gas_json.get(self.prices_names[-1]).get(self.currency)

    def get_w3_instance_with_gas(self):
        gas_price = self.gas_instance.gas_price_selection

        w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 10}))
        if not w3.isConnected():
            raise ConnectionError('Invalid http provider')

        w3.eth.set_gas_price_strategy(gas_price)
        w3.middleware_onion.add(middleware.time_based_cache_middleware)
        w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        w3.middleware_onion.add(middleware.simple_cache_middleware)
        return w3, gas_price

    @staticmethod
    def gas_info():
        _HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/32.0.1667.0 Safari/537.36'
        }

        while True:
            time.sleep(1)
            request = requests.get(
                GAS_ENDPOINT,
                headers=_HEADERS
            )

            if request.status_code == 200:
                break

        return request.json()


class UniSwapWrapper:

    def __init__(self, uniswap: Uniswap, gas_instance=None):
        """
        #
        :param gas_instance: instance with method gas_price_selection
        """
        self.uniswap = uniswap
        self.gas_instance = gas_instance

    def change_slippage(self, max_slippage: float):
        self.uniswap.default_slippage = max_slippage

    def gas_price(self):
        if self.gas_instance is None:
            raise IndentationError('You must add gas_instance on initialization')

        try:
            w3, gas_price = self.gas_instance.get_w3_instance_with_gas()
            self.uniswap.w3 = w3

            return gas_price()

        except Exception:
            raise ModuleNotFoundError(
                'Your class must have gas_price_selection method'
            )

    def get_token_to_price(self, token_input, token_output, quantity: int = 1):
        tki = self.check_address(token_input)
        tko = self.check_address(token_output)

        output = self.uniswap.get_price_input(
            token0=tki.address,
            token1=tko.address,
            qty=quantity * 10 ** tki.decimals,
        )
        price = output / 10 ** tko.decimals
        return price

    def custom_make_trade(self, token_from, token_to, quantity: int = 1):
        token_input = self.check_address(token_from)
        token_output = self.check_address(token_to)

        x = self.uniswap.make_trade(
            token_input.address,
            token_output.address,
            quantity * 10 ** token_input.decimals,
            fee=500
        )

        print(x)


    def check_address(self, token):
        token_address = Web3.toChecksumAddress(token)
        return self.uniswap.get_token(token_address)


