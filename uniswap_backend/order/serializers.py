from rest_framework import serializers

from .models import Order
from .validators import SerializerValidatorMixin


class OrderSerializer(serializers.ModelSerializer, SerializerValidatorMixin):
    class Meta:
        model = Order
        fields = ('token_to', 'to_count', 'token_from', 'from_count', 'percentage', 'start_time', 'end_time')

    def validate(self, attrs):
        attrs['percentage'] = 1 + attrs.get('percentage')
        attrs['token_to'] = self.validate_token_address(attrs['token_to'], 'token_to')
        attrs['token_from'] = self.validate_token_address(attrs['token_from'], 'token_from')
        attrs['start_time'], attrs['end_time'] = self.validate_time_range(attrs['start_time'], attrs['end_time'])
        attrs['to_count'], attrs['from_count'] = self.validate_token_count(attrs['to_count'], attrs['from_count'])
        self.validate_balance(attrs['token_from'], float(attrs['from_count']))
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['contract_address'] = instance.contract_address
        return representation
