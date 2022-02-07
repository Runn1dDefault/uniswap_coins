from decimal import Decimal
from pprint import pprint
from time import sleep
from typing import Union

from django.conf import settings
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from uniswap import Uniswap
from web3.types import Wei

from authentication.models import Wallet
from order.services.utils import get_price
from order.models import Order, OrderPrice, OrderTx


class Trader:
    convert_map = {'1': 'wei', '3': 'kwei', '6': 'mwei', '9': 'gwei', '12': 'szabo', '15': 'finney',
                   '18': 'ether', '21': 'kether', '24': 'mether', '27': 'gether', '30': 'tether'}

    def __init__(self, order: Order):
        _pk = Wallet.objects.get_private_key(order.wallet.address, order.get_ps())
        self.uniswap = Uniswap(address=order.wallet.address,
                               private_key=_pk,
                               version=3,
                               provider=settings.PROVIDER, use_estimate_gas=True, default_slippage=order.slippage)
        self.order = order
        self.tk1 = self.uniswap.w3.toChecksumAddress(order.token_from.address)
        self.tk2 = self.uniswap.w3.toChecksumAddress(order.token_to.address)
        self.sell_price = Decimal('{:f}'.format(order.count_from + (order.count_from / 100 * order.sell_percentage)))
        self.tk1_qty = order.count_from
        self.tk2_qty = order.count_to
        self.qty_tk1 = self.quantity(float(order.count_from), order.token_from.decimals)
        self.qty_tk2 = self.quantity(float(order.count_to), order.token_to.decimals)

    def quantity(self, count, decimal: int) -> int:
        return self.uniswap.w3.toWei(count, self.convert_map[str(decimal)])

    def make_trade(self, tk1: ChecksumAddress, tk2: ChecksumAddress, qty: Union[Wei, int]):
        for fee in (3000, 500, 10000):
            try:
                return self.uniswap.make_trade(tk1, tk2, qty=qty, fee=fee).hex()
            except Exception as e:
                if fee == 10000:
                    raise Exception(e)
                continue

    def check_contract_success(self, tx_hash: HexBytes):
        tx_data = self.uniswap.w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_data.status == 1:
            return True
        return False


def trade_loop_run(order: Order):
    trader = Trader(order)
    # for complete prices
    prices = list()
    # for checked when buy and when sell
    is_buy = False
    is_sell = False
    while 1:
        sleep(5)  # ISP speed limit
        price = get_price(trader.tk1, trader.tk2, order.token_from.chainId, trader.qty_tk1)
        if price:
            price_buy = float(price)
            # price retention
            prices.append(price_buy)
            if len(prices) == 4:
                OrderPrice.objects.create(order=order, max_price=max(prices), min_price=min(prices), open=prices[0],
                                          close=prices[-1])
                prices.clear()
            # buy logic
            if is_buy is False and price_buy >= trader.tk2_qty:
                hash_buy = trader.make_trade(trader.tk1, trader.tk2, trader.qty_tk1)
                OrderTx.objects.create(order=order, tx_hash=hash_buy, type_tx='purchase')
                if trader.check_contract_success(hash_buy):
                    pprint(f'Buy {hash_buy}')
                    is_buy = True
            # sell logic
            if order.only_buy is False and is_buy and is_sell is False:
                sleep(5)  # ISP speed limit
                price_sell = float(get_price(trader.tk2, trader.tk1, order.token_from.chainId, trader.qty_tk2))
                if price_sell >= trader.sell_price:
                    hash_sell = trader.make_trade(trader.tk2, trader.tk1, trader.qty_tk2)
                    OrderTx.objects.create(order=order, tx_hash=hash_sell, type_tx='sale')
                    if trader.check_contract_success(hash_sell):
                        pprint(f'Sell {hash_sell}')
                        is_sell = True
            # stop after transaction or continue
            # WARNING: If you want to stop the process, replace the value order.is_revolving_trade to False
                # Then kill process
            if order.is_revolving_trade:
                if order.only_buy:
                    if is_buy:
                        is_buy = False
                else:
                    if is_buy and is_sell:
                        is_buy = False
                        is_sell = False
            else:
                if (order.only_buy and is_buy) or (order.only_buy is False and is_buy and is_sell):
                    break
