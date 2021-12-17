#!/bin/bash

echo "Waiting for server volume..."
cd uniswap_backend
echo "Maker collectstatic"
./manage.py collectstatic --no-input --clear

echo "Run gunicorn"
./manage.py makemigrations
./manage.py migrate
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin') else print('Nice')"
gunicorn uniswap_backend.wsgi:application --bind 0.0.0.0:8000