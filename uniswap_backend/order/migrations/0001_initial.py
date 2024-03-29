# Generated by Django 4.0.1 on 2022-01-20 14:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_from', models.DecimalField(decimal_places=15, max_digits=19)),
                ('count_to', models.DecimalField(decimal_places=15, max_digits=19)),
                ('percentage', models.DecimalField(decimal_places=10, default=1, max_digits=19)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('contract_address', models.TextField(blank=True)),
                ('task_id', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('In Process', 'Process'), ('Waiting', 'Wait'), ('Success', 'Success'), ('Failed', 'Failed'), ('Over without trade', 'Overwtrade')], default='Waiting', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('address', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Token Name')),
                ('chainId', models.IntegerField()),
                ('decimals', models.PositiveIntegerField()),
                ('symbol', models.CharField(max_length=50)),
                ('logoURI', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=15, max_digits=19)),
                ('mean_price', models.DecimalField(decimal_places=15, max_digits=19)),
                ('max_price', models.DecimalField(decimal_places=15, max_digits=19)),
                ('min_price', models.DecimalField(decimal_places=15, max_digits=19)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 1, 20, 14, 13, 36, 841629, tzinfo=utc))),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='order.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='token_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens_from', to='order.token'),
        ),
        migrations.AddField(
            model_name='order',
            name='token_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens_to', to='order.token'),
        ),
    ]
