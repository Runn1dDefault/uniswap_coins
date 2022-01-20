from collections import OrderedDict

from rest_framework import serializers

from order.models import Order, Token, OrderPrice
from order.validators import ValidatorMixin
from order.utils import time_edit


class OrderSerializer(serializers.ModelSerializer, ValidatorMixin):
    validator_class = serializers.ValidationError
    times = serializers.CharField(min_length=2, required=True)

    class Meta:
        model = Order
        fields = (
            'token_from', 'count_from', 'token_to', 'count_to', 
            'percentage', 'status', 'times'
        )
        extra_kwargs = {
            'token_from': {'required': True},
            'token_to': {'required': True},
            'count_from': {'required': True},
            'count_to': {'required': True},
            'percentage': {'required': True},
            'status': {'required': False}
        }
    
    def validate_percentage(self, percentage):
        self.validate_percentage_(percentage)
        return percentage + 1

    def validate_count_from(self, count_from):
        self.validate_token_count(float(count_from), 'count_from')
        return count_from

    def validate_count_to(self, count_to):
        self.validate_token_count(float(count_to), 'count_to')
        return count_to

    def create(self, validated_data):
        if validated_data.get('token_from') and validated_data.get('count_from'):
            self.check_token_group_balance(validated_data['token_from'], float(validated_data['count_from']))

        validated_data['start_time'], validated_data['end_time'] = time_edit(
            validated_data.pop('times')
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = OrderedDict()
        representation['id'] = instance.id
        representation['tokens'] = f'{instance.token_from.name} -> {instance.token_to.name}'
        representation['prices'] = f'{float(instance.count_from)} -> {float(instance.count_to)}'
        representation['times'] = f'{instance.start_time.strftime("%H:%M:%S %m-%d ")} -> ' \
                                  f'{instance.end_time.strftime("%H:%M:%S %m-%d")}'
        representation['status'] = instance.status
        representation['contract_address'] = instance.contract_address
        return representation


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class OrderPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPrice
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.timestamp()
        return representation
