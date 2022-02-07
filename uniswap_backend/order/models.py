import functools
import os
import json

from django.db import models
from django.conf import settings

from authentication.models import Wallet
from order.services.utils import get_tokens


class Coin(models.Model):
    # do not change field names (if only changed to uniswap)
    address = models.CharField(max_length=50, primary_key=True)
    name, symbol = models.CharField(max_length=255), models.CharField(max_length=50)
    chainId = models.IntegerField()  # Network
    decimals = models.PositiveIntegerField()
    logoURI = models.URLField(blank=True, max_length=700)

    @classmethod
    def get_all_tokens_and_save(cls):
        new_tokens = [cls(**i) for i in get_tokens() if not cls.objects.filter(address=i['address']).exists()]
        if new_tokens:
            cls.objects.bulk_create(new_tokens)

    @classmethod
    def ropsten_tokens_save(cls):
        # for make test txs
        with open(os.path.join(settings.BASE_DIR, 'ropsten_tokens.json')) as file:
            data = json.load(file)
        for token in data:
            if not cls.objects.filter(address=token['address']).exists():
                cls.objects.create(**token)


def _clear_password(method):
    @functools.wraps(method)
    def clear(self, *args, **kwargs):
        ps = method(self, *args, **kwargs)
        self._password = ''
        self.save()
        return ps
    return clear


class Order(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='orders')
    token_from = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='tokens_from')
    count_from = models.DecimalField(max_digits=50, decimal_places=30)
    token_to = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='tokens_to')
    count_to = models.DecimalField(max_digits=50, decimal_places=30)
    sell_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    slippage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.TextField(blank=True)
    only_buy = models.BooleanField(default=False)
    is_revolving_trade = models.BooleanField(default=False)
    # to define the task
    task_id = models.CharField(max_length=255, blank=True)
    _password = models.CharField(max_length=50, blank=True)

    @_clear_password
    def get_ps(self):
        return self._password


class OrderTx(models.Model):
    TYPE_CHOICES = (('purchase', 'Purchase'), ('sale', 'Sale'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='txs')
    tx_hash = models.CharField(max_length=500)
    type_tx = models.CharField(choices=TYPE_CHOICES, max_length=10, default='purchase')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderPrice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='prices')
    open = models.DecimalField(max_digits=50, decimal_places=30)
    close = models.DecimalField(max_digits=50, decimal_places=30)
    max_price = models.DecimalField(max_digits=50, decimal_places=30)
    min_price = models.DecimalField(max_digits=50, decimal_places=30)
    date = models.DateTimeField(auto_now_add=True)
