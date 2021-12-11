import unittest

from uniswap.exceptions import InvalidToken
from uniswap.token import BaseToken

from .instances import uniswap_instance
from .services import UniSwapWrapper, GasWrapper


class TestUniSwapWrapper(unittest.TestCase):
    def setUp(self) -> None:
        self.uniswap = UniSwapWrapper(
            uniswap=uniswap_instance,
            gas_instance=GasWrapper(
                token_output_price=0.00000185811,
                currency='usd'
            )
        )

    def test_get_token(self):
        # BAT
        self.assertIsInstance(
            self.uniswap.get_token('0x0D8775F648430679A709E98d2b0Cb6250d2887EF'),
            BaseToken
        )
        self.assertEqual(
            self.uniswap.get_token('0x0D8775F648430679A709E98d2b0Cb6250d2887EF').name,
            'Basic Attention Token'
        )
        # UNI
        self.assertIsInstance(
            self.uniswap.get_token('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'),
            BaseToken
        )
        self.assertEqual(
            self.uniswap.get_token('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984').name,
            'Uniswap'
        )
        # ENS
        self.assertIsInstance(
            self.uniswap.get_token('0xc18360217d8f7ab5e7c516566761ea12ce7f9d72'),
            BaseToken
        )
        self.assertEqual(
            self.uniswap.get_token('0xc18360217d8f7ab5e7c516566761ea12ce7f9d72').name,
            'Ethereum Name Service'
        )
        # ETH
        self.assertRaises(
            InvalidToken,
            self.uniswap.get_token,
            token='0x0000000000000000000000000000000000000000'
        )
        # USDT
        self.assertIsInstance(
            self.uniswap.get_token('0xdac17f958d2ee523a2206206994597c13d831ec7'),
            BaseToken
        )
        self.assertEqual(
            self.uniswap.get_token('0xdac17f958d2ee523a2206206994597c13d831ec7').name,
            'Tether USD'
        )

    # def test_get_token_to_price(self):
    #     # ETH -> USTD
    #     price = self.uniswap.get_token_to_price(
    #         token_from='0xdac17f958d2ee523a2206206994597c13d831ec7',
    #         token_to='0x0000000000000000000000000000000000000000'
    #     )
    #     self.assertIsInstance(price, float)

    def test_gas_price(self):
        price = self.uniswap.gas_price()
        print(price)
        self.assertIsInstance(price, float)
