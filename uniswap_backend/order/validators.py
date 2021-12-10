import datetime
from typing import Union

from django.utils.timezone import localtime, now
from rest_framework import serializers
from web3 import Web3


def validate_percentage(value: Union[int, float]):
    if value < 0 or value > 100:
        raise ValueError('Invalid percentage: {}'.format(value))


class SerializerValidatorMixin:
    @staticmethod
    def validate_token_address(token_address: str, field_name: str):
        try:
            Web3.toChecksumAddress(token_address)
            return token_address
        except Exception:
            raise serializers.ValidationError({field_name: 'Invalid token address!'})

    @staticmethod
    def validate_token_count(to_count: Union[float, int], from_count: Union[int, float]):
        if to_count == 0:
            raise serializers.ValidationError(
                {
                    'to_count': 'must be greater than zero'
                }
            )
        if from_count == 0:
            raise serializers.ValidationError(
                {
                    'from_count': 'must be greater than zero'
                }
            )
        return to_count, from_count

    @staticmethod
    def validate_time_range(start_time: datetime, end_time: datetime):

        if end_time > localtime(now()) < start_time < end_time:
            return start_time, end_time

        raise serializers.ValidationError(
            {'start_time': 'Invalid time range', 'end_time': 'Invalid time range'}
        )
