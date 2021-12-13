# Generated by Django 4.0 on 2021-12-10 13:37

from django.db import migrations, models
import order.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_to', models.CharField(max_length=255)),
                ('token_from', models.CharField(max_length=255)),
                ('from_count', models.DecimalField(decimal_places=10, max_digits=19)),
                ('to_count', models.DecimalField(decimal_places=10, max_digits=19)),
                ('percentage', models.DecimalField(decimal_places=10, default=1, max_digits=19, validators=[order.validators.validate_percentage])),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]