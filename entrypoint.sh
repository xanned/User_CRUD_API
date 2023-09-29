#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      echo "Waiting for db to be ready..."
      sleep 0.1
    done
fi
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput
python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
gunicorn --bind 0.0.0.0:8000 user_api.wsgi -w 4