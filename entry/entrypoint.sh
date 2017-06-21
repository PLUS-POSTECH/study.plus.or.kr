#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate

if [ "${DJANGO_DEBUG,,}" = "true" ]; then
    echo "Django debug is on"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Django debug is off"
    python manage.py collectstatic --noinput
    gunicorn plus_study.wsgi -b 0.0.0.0:8000
fi
