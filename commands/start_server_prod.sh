#!/bin/bash

python /store/src/manage.py makemigrations
python /store/src/manage.py migrate

python /store/src/manage.py collectstatic --noinput

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src config.wsgi:application --reload --log-level=${WSGI_LOG_LEVEL}