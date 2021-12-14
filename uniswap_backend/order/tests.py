import datetime

from django.urls import reverse, path
from django.utils.timezone import localtime, now
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import Order
from .views import OrderModelViewSet


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
        today = localtime(now()) + datetime.timedelta(minutes=5)
        self.order = Order.objects.create(
            token_from='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            token_to='0xdAC17F958D2ee523a2206206994597C13D831ec7',
            from_count=1,
            to_count=4000.45,
            percentage=1,
            start_time=today,
            end_time=today + datetime.timedelta(days=1)
        )

    def test_order_create(self):
        url = reverse('order_list')
        # ETH=1 -> USDT=3804.45
        today = localtime(now()) + datetime.timedelta(minutes=5)

        data = dict(
            token_from='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            token_to='0xdAC17F958D2ee523a2206206994597C13D831ec7',
            from_count=1,
            to_count=4000.45,
            percentage=1,
            start_time=today,
            end_time=today + datetime.timedelta(days=1)
        )

        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['token_from'] = '0x0x0x00x0x'
        data['start_time'] = localtime(now())
        response = self.client.post(url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

