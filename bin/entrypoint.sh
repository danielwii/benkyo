#!/bin/bash

#set -e

python manage.py migrate
python manage.py load_chapters

echo $@

exec "$@"
