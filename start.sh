#!/bin/sh
python manage.py collectstatic --no-input
export CURRENT_EVENT_PK="c16853ea-5fd4-4f97-adc2-1db50ef06abc"
if [ "$APP_MODE" = "custom-command" ]
  then
    python manage.py "$APP_COMMAND"
  fi
  # do standard start
if [ "$APP_MODE" = "wsgi" ]
  then
  gunicorn ply.wsgi:application -b 0.0.0.0:8001
fi
if [ "$APP_MODE" = "celery" ]
  then
  celery -A ply worker -l INFO --without-heartbeat --without-gossip --without-mingle
fi