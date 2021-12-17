import unittest

from django.conf import settings

from uniswap.exceptions import InvalidToken, InsufficientBalance
from uniswap.token import BaseToken

from order.services.instances import get_uniswap_instance
from order.services.services import UniSwapWrapper
from order.services.convert import token_check_address


class TestTokenCheck(unittest.TestCase):
    def setUp(self) -> None:
        # test with main network
        self.uniswap_instance = get_uniswap_instance()

    def test_base_token(self):
        base_token, decimal = token_check_address(settings.BASE_TOKEN_ADDRESS, True)
        self.assertEqual(decimal, 18)
        self.assertIsInstance(base_token, str)
        self.assertRaises(InvalidToken, self.uniswap_instance.get_token, address=base_token)

    def test_defi_token(self):
        """
            Test some polarized tokens
        """
        uniswap, uniswap_decimals = token_check_address('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', True)
        self.assertEqual(uniswap_decimals, 18)
        self.assertIsInstance(uniswap, BaseToken)
        sushi, sushi_decimals = token_check_address('0x6b3595068778dd592e39a122f4f5a5cf09c90fe2', True)
        self.assertEqual(sushi_decimals, 18)
        self.assertIsInstance(sushi, BaseToken)
        wbtc, wbtc_decimals = token_check_address('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', True)
        self.assertEqual(wbtc_decimals, 8)
        self.assertIsInstance(wbtc, BaseToken)
        comp, comp_decimals = token_check_address('0xc00e94cb662c3520282e6f5717214004a7f26888', True)
        self.assertEqual(comp_decimals, 18)
        self.assertIsInstance(comp, BaseToken)
        link, link_decimals = token_check_address('0x514910771af9ca656af840dff83e8264ecf986ca', True)
        self.assertEqual(link_decimals, 18)
        self.assertIsInstance(link, BaseToken)


class TestUniswapWrapper(unittest.TestCase):
    def setUp(self) -> None:
        # ETH -> UNI
        self.uniswap = UniSwapWrapper(
            token_from=settings.BASE_TOKEN_ADDRESS,
            token_to='0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',
            from_count=0.1007,
            to_count=1.15113,
            percentage=1,
            # change provider on test network
            is_test=True
        )
        self.balance = self.uniswap.uniswap.get_token_balance(self.uniswap.token_from)

    def test_get_token_to_price(self):
        price = self.uniswap.get_token_to_price
        self.assertIsInstance(price, float)
        self.assertNotEqual(price, 0)

    def test_price_in_range(self):
        result = self.uniswap.price_in_range
        self.assertIsInstance(result, bool)

    def test_make_trade(self):
        if self.balance <= 0:
            self.assertRaises(InsufficientBalance, self.uniswap.make_trade)
        else:
            contract_address = self.uniswap.make_trade()
            self.assertIsInstance(contract_address, str)
            contract = self.uniswap.uniswap.w3.eth.contract(contract_address)
            self.assertNotEqual(contract, None)

    def test_max_slippage(self):
        max_slippage = self.uniswap.max_slippage
        self.assertIsInstance(max_slippage, float or int)

        max_slippage_must = self.uniswap.price * self.uniswap.percentage / 100
        self.assertEqual(max_slippage, max_slippage_must)
