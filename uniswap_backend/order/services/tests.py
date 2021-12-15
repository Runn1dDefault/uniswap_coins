import unittest
from decimal import Decimal

from uniswap import Uniswap
from uniswap.exceptions import InvalidToken
from uniswap.token import BaseToken
from web3 import Web3

from .instances import uniswap_instance, ADDRESS, PRIVATE_KEY
from .services import UniSwapWrapper, SwapWrapper


class TestUniswapWrapper(unittest.TestCase):
    def setUp(self) -> None:
        self.uniswap = UniSwapWrapper(
            uniswap=uniswap_instance
        )

    # def test_check_address(self):
    #     # UNI
    #     address = self.uniswap.check_address('0x9bc74DD43970b43ea94760A24043bBe2089A670B')
    #
    #     self.assertIsInstance(
    #         self.uniswap.check_address('0x9bc74DD43970b43ea94760A24043bBe2089A670B'),
    #         BaseToken
    #     )
    #     self.assertEqual(
    #         self.uniswap.check_address('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984').name,
    #         'Uniswap'
    #     )
    #     # ETH
    #     # This base address 0x0000000000000000000000000000000000000000
    #     # Valid address 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
    #     self.assertRaises(
    #         InvalidToken,
    #         self.uniswap.check_address,
    #         token='0x0000000000000000000000000000000000000000'
    #     )
    #     self.assertRaises(
    #         ValueError,
    #         self.uniswap.check_address,
    #         token='0x0000000000000000'
    #     )
    #
    def test_get_token_to_price(self):
        # UNI=2 -> ETH -> USTD
        price = self.uniswap.get_token_to_price(
            token_input='0x0000000000000000000000000000000000000000',
            token_output='0xc8f88977e21630cf93c02d02d9e8812ff0dfc37a',
            quantity=2
        )
        print(price)

        self.assertIsInstance(price, float)
    #
    # def test_gas_price(self):
    #     self.uniswap.change_gas_strategy()
    #
    #     price = Web3.fromWei(self.uniswap.uniswap.w3.eth.generate_gas_price(), 'gwei')
    #
    #     self.assertIsInstance(price, Decimal)


class TestSwapWrapper(unittest.TestCase):
    def setUp(self) -> None:

        # ETH=0.3 -> USTD
        self.wrapper = SwapWrapper(
            token_from='0xc8f88977e21630cf93c02d02d9e8812ff0dfc37a',
            token_to='0x0000000000000000000000000000000000000000',
            from_count=0.001,
            to_count=4000.45,
            percentage=1
        )

        # Ropsten test network
        self.wrapper.uni_wrapper = UniSwapWrapper(
            uniswap=Uniswap(
                provider='https://ropsten.infura.io/v3/d6dc1928fa734842bb81ce889a2f7e8b',
                address=ADDRESS,
                private_key=PRIVATE_KEY,
                version=2
            )
        )

    # def test_price_in_range(self):
    #     result = self.wrapper.price_in_range
    #
    #     self.assertIsInstance(result, bool)
    #
    # def test_balance(self):
    #     eth_balance = self.wrapper.eth_balance
    #     print('balance', eth_balance)
    #     self.assertGreater(eth_balance, 0)
    #
    #     token = self.wrapper.uni_wrapper.check_address('0xc778417e063141139fce010982780140aa0cd5ab')
    #
    #     token_balance = self.wrapper.uni_wrapper.uniswap.get_token_balance(token.address)
    #
    #     print('token_balance', token_balance / 10 ** token.decimals)
    #     self.assertGreater(token_balance, 0)
    #
    # def test_max_slippage(self):
    #     max_slippage = self.wrapper.max_slippage
    #     self.assertIsInstance(max_slippage, float or int)
    #
    #     max_slippage_must = self.wrapper.price * self.wrapper.percentage / 100
    #     self.assertEqual(max_slippage, max_slippage_must)
    #
    # def test_max_and_min_price(self):
    #     max_price, min_price = self.wrapper.max_and_min_price
    #     self.assertIsInstance(max_price, float or int)
    #     self.assertIsInstance(min_price, float or int)
    #
    #     max_must = self.wrapper.price + self.wrapper.max_slippage
    #     min_must = self.wrapper.price - self.wrapper.max_slippage
    #     self.assertEqual(max_must, max_price)
    #     self.assertEqual(min_must, min_price)

    # def test_make_trade(self):
    #     print(self.wrapper.make_trade_custom())
