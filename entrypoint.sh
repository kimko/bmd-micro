#!/bin/sh
# During image startup for test/dev wait for postgres before
# starting the flask server

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0