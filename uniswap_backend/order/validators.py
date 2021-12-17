import datetime
from typing import Union

from django.utils.timezone import localtime, now
from django import forms

from order.services.convert import token_check_address
from order.services.instances import get_uniswap_instance


class ValidatorMixin:
    @staticmethod
    def validate_percentage(value: Union[int, float]):
        if value < 0 or value > 100:
            raise forms.ValidationError({'percentage': 'Invalid percentage: {}'.format(value)})

    @staticmethod
    def validate_token_address(token_address, filed_name: str):
        try:
            token_check_address(token_address)
        except Exception:
            raise forms.ValidationError({filed_name: 'Invalid token address!'})

    @staticmethod
    def validate_token_count(to_count: Union[float, int], from_count: Union[int, float]):
        if to_count == 0:
            raise forms.ValidationError({'to_count': 'Must be greater than zero'})
        if from_count == 0:
            raise forms.ValidationError({'from_count': 'Must be greater than zero'})

    @staticmethod
    def validate_time_range(start_time: datetime, end_time: datetime):
        if localtime(now()) - datetime.timedelta(seconds=20) > start_time:
            raise forms.ValidationError({'start_time': 'Invalid time range'})
        if start_time > end_time:
            raise forms.ValidationError({'end_time': 'Invalid time range'})

    def check_token_group_balance(self, token_from: str = None, from_count: Union[int, float] = None):
        """
            Balance check with pairs that are not over yet
        """
        # is not a test network
        if token_from and from_count:
            uniswap_instance = get_uniswap_instance()
            token_address, token_decimals = token_check_address(token_from)
            orders = self.__class__.objects.filter(
                contract_address='',
                end_time__gt=localtime(now()),
                token_from=token_address
            )
            tokens_quantity = float(sum(i.from_count for i in orders or [])) + from_count

            token_balance = uniswap_instance.get_token_balance(token_address) / 10 ** token_decimals
            # check balance
            if token_balance == 0 or tokens_quantity > token_balance:
                raise forms.ValidationError(
                    f"Insufficient balance for token address: {token_from}.\nToken balance: {token_balance}"
                )
