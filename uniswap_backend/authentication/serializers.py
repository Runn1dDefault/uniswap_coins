from collections import OrderedDict

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, max_length=255, required=True)
    password = serializers.CharField(write_only=True, max_length=255, required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username = validated_data['username']
        password = validated_data['password']
        request_user = get_user_model().objects.get(username=username)
        if not request_user.is_active:
            raise serializers.ValidationError({'details': 'This user is not active'})
        user = authenticate(username=request_user.username, password=password)
        if user is None:
            raise serializers.ValidationError({"details": "Invalid Data"})
        refresh = RefreshToken.for_user(user=user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def to_representation(self, instance):
        res = OrderedDict()
        res['refresh'] = instance['refresh']
        res['access'] = instance['access']
        return res
