import requests


from .decorators import multiprocess, real_support
from .instances import uniswap_instance, web3_instance, GAS_ENDPOINT


class UniSwapWrapper:

    def __init__(self,
                 token_from, token_to,
                 output_price: float,
                 max_slippage: float = 0.1
                 ):
        self.token_from = self.get_token(token_from)
        self.token_to = self.get_token(token_to)

        self.output_price = output_price
        self.max_slippage = max_slippage

    def gas_price(self):
        gas = Gas(self.output_price, 'usd')
        return gas.gas_max_price()

    @real_support
    def get_token_to_price(self):

        output = uniswap_instance.get_price_output(
            self.token_to.address,
            self.token_from.address,
            10 ** self.token_to.decimals
        )

        return '${:,.2f}'.format(
            output / 10 ** self.token_from.decimals
        )

    @real_support
    def get_token(self, token):
        token_address = web3_instance.toChecksumAddress(token)
        return uniswap_instance.get_token(token_address)


class Gas:
    # hierarchy is respected
    prices_names = ('slow', 'normal', 'fast', 'instant')
    price_currency = ('gwei', 'usd')

    def __init__(self, output_price: float, currency: str):
        self.prices_count = len(self.prices_names)
        self.output_price = output_price
        self.currency = currency.strip().lower()
        self._check_currency()

    def _check_currency(self):
        if self.currency not in self.price_currency:
            raise ValueError(f'Currency must be in {self.price_currency}')

    def gas_price_selection(self):
        gas_json = self.gas_info()

        while True:
            for name in list(reversed(self.prices_names)):
                price = gas_json.get(name).get(self.currency)

                if self.output_price > price:
                    return price

    def gas_max_price(self):
        gas_json = self.gas_info()
        return gas_json.get(self.prices_names[-1])

    @staticmethod
    def gas_info():
        _HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/32.0.1667.0 Safari/537.36'
        }

        while True:
            request = requests.get(
                GAS_ENDPOINT,
                headers=_HEADERS
            )

            if request.status_code == 200:
                return request.json()
