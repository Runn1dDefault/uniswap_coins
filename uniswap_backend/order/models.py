from django.db import models

from order.validators import ValidatorMixin


class Order(models.Model, ValidatorMixin):
    # tokens addresses
    token_to = models.CharField(max_length=255)
    token_from = models.CharField(max_length=255)
    # value for tokens
    from_count = models.DecimalField(max_digits=19, decimal_places=10)
    to_count = models.DecimalField(max_digits=19, decimal_places=10)
    # admissible error
    percentage = models.DecimalField(default=1, max_digits=19, decimal_places=10)
    # work timerange
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # for after successful completion of the transaction
    contract_address = models.TextField(blank=True)
    # to define the task
    task_id = models.CharField(max_length=255, blank=True)

    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)

    def clean(self):
        self.validate_percentage(float(self.percentage))
        self.validate_token_address(self.token_to, 'token_to')
        self.validate_token_address(self.token_from, 'token_from')
        self.validate_time_range(self.start_time, self.end_time)
        self.validate_token_count(float(self.to_count), float(self.from_count))
        self.check_token_group_balance(self.token_from, float(self.from_count))

    @classmethod
    def find_and_status_update(cls, contract_address: str, **kwargs):
        objs_filter = cls.objects.filter(**kwargs)
        if objs_filter.exists():
            order = objs_filter.first()
            order.contract_address = contract_address
            order.save()
