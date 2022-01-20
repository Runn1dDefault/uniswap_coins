import json

from django.db import models
from django.utils.timezone import now, localtime


class Token(models.Model):
    address = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Token Name')
    chainId = models.IntegerField()
    decimals = models.PositiveIntegerField()
    symbol = models.CharField(max_length=50)
    logoURI = models.URLField(blank=True)

    @classmethod
    def create_from_json_file(cls):
        with open('tokens.json') as file:
            json_data = json.load(file)

        if json_data:
            new_objs = list(cls(**i) for i in json_data['tokens'] or []
                            if not cls.objects.filter(address=i['address']).exists()
                            )
            if new_objs:
                cls.objects.bulk_create(new_objs)


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PROCESS = 'In Process'
        WAIT = 'Waiting'
        SUCCESS = 'Success'
        FAILED = 'Failed'
        OVERWTRADE = 'Over without trade'

    token_from = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='tokens_from')
    count_from = models.DecimalField(max_digits=19, decimal_places=15)
    token_to = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='tokens_to')
    count_to = models.DecimalField(max_digits=19, decimal_places=15)
    percentage = models.DecimalField(default=1, max_digits=19, decimal_places=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # for after successful completion of the transaction
    contract_address = models.TextField(blank=True)
    # to define the task
    task_id = models.CharField(max_length=255, blank=True)
    
    status = models.CharField(
        max_length=18,
        choices=StatusChoices.choices,
        default=StatusChoices.WAIT,
    )

    def save_contact(self, contract_address):
        self.contract_address = contract_address
        self.status = Order.StatusChoices.SUCCESS
        self.save()


class OrderPrice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=19, decimal_places=15)
    mean_price = models.DecimalField(max_digits=19, decimal_places=15)
    max_price = models.DecimalField(max_digits=19, decimal_places=15)
    min_price = models.DecimalField(max_digits=19, decimal_places=15)
    date = models.DateTimeField(default=localtime(now()))
