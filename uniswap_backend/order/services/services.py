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

    def __init__(self, token_output_price: float, currency: str):
        self.prices_count = len(self.prices_names)
        self.token_output_price = token_output_price
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

            if price > self.token_output_price:
                return price

        return gas_json.get('normal').get(self.currency)

    @multiprocess
    def gas_max_price(self):
        gas_json = self.gas_info()
        return gas_json.get(self.prices_names[-1]).get(self.currency)

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
            gas_price = self.gas_instance.gas_price_selection
            w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 10}))
            w3.eth.set_gas_price_strategy(gas_price)
            self.uniswap.w3 = w3
            return gas_price()

        except Exception:
            raise ModuleNotFoundError(
                'Your class must have gas_price_selection method'
            )

    def get_token_to_price(self, token_from, token_to, quantity: int = 1):
        token_to = self.check_address(token_to)
        token_from = self.check_address(token_from)

        token_out_amount = quantity * 10 ** token_from.decimals

        output = self.uniswap.get_price_output(
            token_to.address,
            token_from.address,
            token_out_amount,
        )
        price = output / 10 ** token_to.decimals
        return price

    def check_address(self, token):
        token_address = Web3.toChecksumAddress(token)
        return self.uniswap.get_token(token_address)
