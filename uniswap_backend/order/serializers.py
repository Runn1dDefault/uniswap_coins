from collections import OrderedDict

from rest_framework import serializers

from order.models import Order, Coin, OrderPrice, OrderTx


class OrderSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, min_length=1)

    class Meta:
        model = Order
        fields = ('token_from', 'count_from', 'token_to', 'count_to', 'status',
                  'only_buy', 'is_revolving_trade', 'sell_percentage', 'slippage', 'password')
        extra_kwargs = {
            'token_from': {'required': True},
            'token_to': {'required': True},
            'count_from': {'required': True},
            'count_to': {'required': True},
            'status': {'required': False}
        }

    def validate_slippage(self, slippage):
        if slippage > 1 or slippage <= 0:
            raise serializers.ValidationError('In range 0.1 to 1')
        return slippage

    def validate_sell_percentage(self, sell_percentage):
        if sell_percentage > 100 or sell_percentage <= 0:
            raise serializers.ValidationError('In range 1 to 100')
        return sell_percentage

    def validate_count_from(self, count_from):
        if count_from <= 0:
            raise serializers.ValidationError('Must be > 0')
        return count_from

    def validate_count_to(self, count_to):
        if count_to <= 0:
            raise serializers.ValidationError('Must be > 0')
        return count_to

    def create(self, validated_data):
        query = self.context['request'].user.wallets.all()
        if not query.exists():
            raise serializers.ValidationError({'detail': 'You forgot to add wallet data'})
        wallet = query.order_by('created_at').last()
        password = validated_data.pop('password')
        if not wallet.user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password!'})
        validated_data['wallet'] = wallet
        return self.Meta.model.objects.create(**validated_data, _password=password)

    def to_representation(self, instance):
        representation = OrderedDict()
        representation['id'] = instance.id
        representation['tokens'] = f'{instance.token_from.name} -> {instance.token_to.name}'
        representation['prices'] = f'{float(instance.count_from)} -> {float(instance.count_to)}'
        representation['status'] = instance.status
        return representation


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class OrderPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPrice
        fields = '__all__'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        r['date'] = instance.date.timestamp()
        return r


class OrderTxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTx
        fields = '__all__'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        r['created_at'] = instance.created_at.strftime('%H:%M %m/%d/%y')
        return r
