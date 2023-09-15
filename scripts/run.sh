#! /bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin
python manage.py adminplus_init

uwsgi --socket :9000 --workers 4 --master --enable-threads --module _LGM.wsgi
