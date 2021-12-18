from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('token_from', 'count_from', 'token_to', 'count_to', 'contract_address')
