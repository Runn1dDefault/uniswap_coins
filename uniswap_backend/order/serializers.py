from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('token_from', 'count_from', 'token_to', 'count_to', 'percentage', 'start_time', 'end_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['contract_address'] = instance.contract_address
        return representation
