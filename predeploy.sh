#!/bin/bash

cd /app

python manage.py collectstatic --noinput -v 0
python manage.py compress -v 0
python manage.py collectstatic --noinput -v 0
python manage.py migrate
