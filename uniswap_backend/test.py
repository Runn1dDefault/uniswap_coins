import datetime

from django.utils.timezone import now, localtime
from django.conf import settings


today = localtime(now()) + datetime.timedelta(seconds=1)
data = dict(token_from=settings.BASE_TOKEN_ADDRESS, token_to='0xc8f88977e21630cf93c02d02d9e8812ff0dfc37a', from_count=0.1007, to_count=1.15113, percentage=1, start_time=today,end_time=today + datetime.timedelta(days=1))
