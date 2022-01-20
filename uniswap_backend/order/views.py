import re

from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import Order, Token
from order.serializers import OrderSerializer, TokenSerializer, OrderPricesSerializer
from order.tasks import swap_task
from order.utils import time_edit, check_task

from uniswap_backend.celery import app


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['GET'], detail=True)
    def order_prices(self, request, pk=None):
        order = self.get_object()
        prices = order.prices.all().order_by('date')
        serializer = OrderPricesSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def stop_task(self, request, pk=None):
        order = self.get_object()
        if order.contract_address and order.status == Order.StatusChoices.SUCCESS:
            return Response({'details': 'order is overed!'}, status=status.HTTP_304_NOT_MODIFIED)

        task_id = order.task_id

        if task_id and check_task(task_id):
            app.control.revoke(task_id, terminate=True)
            if not order.contract_address:
                order.status = Order.StatusChoices.OVERWTRADE
                order.save()
            else:
                order.status = Order.StatusChoices.SUCCESS
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def start_task(self, request, pk=None):

        times = request.data.get('times')
        if not times:
            return Response({'times': 'Required for start order'}, status=status.HTTP_304_NOT_MODIFIED)
        elif not re.findall(r'\d+', times):
            return Response({'times': 'Invalid times!'}, status=status.HTTP_304_NOT_MODIFIED)

        order = self.get_object()
        # times update
        start_time, end_time = time_edit(times)
        order.start_time, order.end_time = start_time, end_time
        order.save()
        # start new task
        task = swap_task.apply_async(kwargs={'order_id': order.id}, eta=start_time)
        order.task_id = task.task_id
        order.status = Order.StatusChoices.WAIT
        order.save()
        return Response(status.HTTP_200_OK)


class TokenModelViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('query')
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) | 
            Q(symbol__icontains=query)
        )
        serializer = self.get_serializer(queryset[:20], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
