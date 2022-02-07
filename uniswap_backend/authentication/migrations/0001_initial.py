# Generated by Django 4.0.2 on 2022-02-03 11:36

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('address', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('private_key', models.BinaryField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('objects', authentication.models.WalletManager()),
            ],
        ),
    ]
