import datetime

from django.urls import reverse, path
from django.utils.timezone import localtime, now
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from order.models import Order
from order.views import OrderModelViewSet


class OrderTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path(
            'api/order/',
            OrderModelViewSet.as_view(
                {'post': 'create', 'get': 'list'}
            ),
            name='order_list'
        ),
        path(
            'api/order/<int:pk>/',
            OrderModelViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
            }),
            name='order_detail'
        ),
    ]

    def setUp(self) -> None:
        today = localtime(now()) - datetime.timedelta(seconds=30)
        self.order = Order.objects.create(
            token_from='0x0000000000000000000000000000000000000000',
            count_from=0.001,
            token_to='0xc8f88977e21630cf93c02d02d9e8812ff0dfc37a',
            count_to=4000.45,
            percentage=1,
            start_time=today,
            end_time=today + datetime.timedelta(days=1)
        )

    def test_order_create(self):
        url = reverse('order_list')
        # ETH=1 -> USDT=3804.45
        today = localtime(now()) + datetime.timedelta(seconds=1)

        data = dict(
            token_from=settings.BASE_TOKEN_ADDRESS,
            count_from=0.01,
            token_to='0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
            count_to=0.00190652,
            percentage=1,
            start_time=today,
            end_time=today + datetime.timedelta(days=1)
        )

        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list(self):
        url = reverse('order_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.order.token_from, response.data[0].get('token_from'))
        self.assertEqual(self.order.token_to, response.data[0].get('token_to'))

    def test_order_read(self):
        url = reverse('order_detail', kwargs={'pk': self.order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_delete(self):
        url = reverse('order_detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
