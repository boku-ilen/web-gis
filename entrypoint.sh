#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=admin python3 manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000
