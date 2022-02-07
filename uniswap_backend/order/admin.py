from django.contrib import admin

from order.models import Order, OrderPrice, Coin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('token_from', 'count_from', 'token_to', 'count_to')


@admin.register(OrderPrice)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'open', 'max_price', 'min_price', 'close', 'date')


@admin.register(Coin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'chainId', 'symbol', 'decimals', 'address', 'logoURI')
