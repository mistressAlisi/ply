#!/bin/bash
cat /etc/banner/dragon
cat /etc/banner/ply
cd /app
echo "•--» Bringing Database up to date (migrate/SQL files)... "
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py install_sql_files _all_
echo "•--» Starting NGINX ... "
/etc/init.d/nginx start
echo "•--» Starting RABBITMQ ... "
/etc/init.d/rabbitmq-server start

echo "•--» Starting Celery ... "
python3 -m celery -A ply.celery worker --uid www-data --gid www-data &
/usr/bin/uwsgi --reload-on-exception --uid www-data --gid www-data --master --emperor /etc/uwsgi/apps-enabled/ --plugin python3 --enable-threads