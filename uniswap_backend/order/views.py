from pprint import pprint

from django.db.models import Q
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission

from order.models import Order, Coin
from order.tasks import swap_task
from order.serializers import (OrderSerializer, TokenSerializer, OrderPricesSerializer, OrderTxSerializer, serializers)

from uniswap_backend.celery import app


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user is obj.wallet.user


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    perm = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return self.queryset.filter(wallet__user=self.request.user)

    def _validate_field(self, field: str):
        result = self.request.data.get(field, None)
        if not result:
            raise serializers.ValidationError({field: 'Required!'})
        return result

    def _get_order(self) -> tuple:
        order_id = self._validate_field('order_id')
        query = self.get_queryset().filter(id=order_id)
        if not query.exists():
            raise serializers.ValidationError({'order_id': 'Not found!'})
        order = query.first()
        password = self._validate_field('password')
        if not order.wallet.user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password!'})
        return order, password

    @action(methods=['GET'], detail=True)
    def order_prices(self, request, pk=None):
        order = self.get_object()
        prices = order.prices.all().order_by('date')
        serializer = OrderPricesSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def order_txs(self, request, pk=None):
        order = self.get_object()
        txs = order.txs.all().order_by('created_at', 'type_tx')
        serializer = OrderTxSerializer(txs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def stop_task(self, request, pk=None):
        try:
            order, password = self._get_order()
        except serializers.ValidationError as serialize_error:
            return Response(serialize_error, status=status.HTTP_409_CONFLICT)

        try:
            app.control.revoke(order.task_id, terminate=True)
            order.status = 'Stopped'
            order.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            pprint(e)
            return Response({'detail': 'Task is not running before!'}, status=status.HTTP_304_NOT_MODIFIED)

    @action(methods=['POST'], detail=False)
    def start_task(self, request, pk=None):
        try:
            order, password = self._get_order()
        except serializers.ValidationError as serialize_error:
            return Response(serialize_error, status=status.HTTP_409_CONFLICT)
        # start new task
        task = swap_task.apply_async(kwargs={'order_id': order.id}, eta=timezone.now() + timezone.timedelta(seconds=15))
        order.task_id, order.status, order.password = task.task_id, 'Awaiting launch...', password
        order.save()
        return Response(status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def destroy_order(self, request, *args, **kwargs):
        try:
            order, _ = self._get_order()
        except serializers.ValidationError as serialize_error:
            return Response(serialize_error, status=status.HTTP_409_CONFLICT)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenModelViewSet(ModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('query')
        queryset = self.get_queryset().filter(Q(name__icontains=query) | Q(symbol__icontains=query.upper()))
        serializer = self.get_serializer(queryset[:20], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
