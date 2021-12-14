import unittest

from uniswap.exceptions import InvalidToken
from uniswap.token import BaseToken
from web3 import Web3

from .instances import uniswap_instance
from .services import UniSwapWrapper


class TestUniSwapWrapper(unittest.TestCase):
    def setUp(self) -> None:
        self.uniswap = UniSwapWrapper(
            uniswap=uniswap_instance
        )

    def test_check_address(self):
        # UNI
        self.assertIsInstance(
            self.uniswap.check_address('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'),
            BaseToken
        )
        self.assertEqual(
            self.uniswap.check_address('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984').name,
            'Uniswap'
        )
        # ETH
        self.assertRaises(
            InvalidToken,
            self.uniswap.check_address,
            token='0x0000000000000000000000000000000000000000'
        )
        self.assertRaises(
            ValueError,
            self.uniswap.check_address,
            token='0x0000000000000000'
        )

    def test_get_token_to_price(self):
        # ETH=2 -> USTD
        price = self.uniswap.get_token_to_price(
            token_input='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            token_output='0xc18360217d8f7ab5e7c516566761ea12ce7f9d72',
            quantity=2
        )

        self.assertIsInstance(price, float)

    def test_gas_price(self):
        self.uniswap.change_gas_strategy()
        print(1, Web3.fromWei(self.uniswap.uniswap.w3.eth.generate_gas_price(), 'gwei'))

        print(2, Web3.fromWei(self.uniswap.uniswap.w3.eth.gas_price, 'gwei'))
