from django.db import models

from order.validators import validate_percentage


class Order(models.Model):
    # token address
    token_to = models.CharField(max_length=255)
    token_from = models.CharField(max_length=255)

    # value for tokens
    from_count = models.DecimalField(max_digits=19, decimal_places=10)
    to_count = models.DecimalField(max_digits=19, decimal_places=10)

    # admissible error
    percentage = models.DecimalField(
        default=1,
        max_digits=19,
        decimal_places=10,
        validators=[validate_percentage]
    )
    # work timerange
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # True if work done
    status = models.BooleanField(default=False)

    @classmethod
    def find_and_status_update(cls, **kwargs):
        objs_filter = cls.objects.filter(**kwargs)
        if objs_filter.exists():
            order = objs_filter.first()
            order.status = True
            order.save()
