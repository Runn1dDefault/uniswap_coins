# Generated by Django 4.0 on 2021-12-16 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='contract_address',
            field=models.TextField(blank=True),
        ),
    ]
