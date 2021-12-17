from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('token_from', 'token_to', 'from_count', 'to_count', 'contract_address')
