import datetime

from django.utils.timezone import localtime, now
from django import forms

from typing import Union

from order.services.instances import get_uniswap_instance
from order.models import Order


class ValidatorMixin:
    validator_class = forms.ValidationError
    uniswap_instance = get_uniswap_instance()

    def validate_percentage_(self, value: Union[int, float]):
        if value < 0 or value > 100:
            raise self.validator_class({'percentage': 'Invalid percentage: {}'.format(value)})

    def validate_token_count(self, count: Union[int, float], field: str):
        if count <= 0:
            raise self.validator_class({field: 'Must be greater than zero'})

    def validate_time_range(self, start_time: datetime, end_time: datetime):
        if start_time > end_time:
            raise self.validator_class('Invalid time range')
        
    def check_token_group_balance(self, token_from: str = None, count_from: Union[int, float] = None):
        """
            Balance check with pairs that are not over yet
        """
        # is not a test network
        if token_from and count_from:
            token_address, token_decimals = token_from.address, token_from.decimals
            orders = Order.objects.filter(
                contract_address='',
                end_time__gt=localtime(now()),
                token_from=token_address
            )
            tokens_quantity = float(sum(i.count_from for i in orders or [])) + count_from
            token_balance = self.uniswap_instance.get_token_balance(token_address) / 10 ** token_decimals
            # check balance
            if token_balance == 0 or tokens_quantity > token_balance:
                raise self.validator_class(
                    {'detail': f"{token_from.name}.\nToken balance: {token_balance}"}
                )
