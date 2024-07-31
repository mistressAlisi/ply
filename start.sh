#!/bin/sh
python manage.py collectstatic --no-input
export CURRENT_EVENT_PK="d1245410-08b0-457c-9439-d6b1f1345ba8"
if [ "$APP_MODE" = "custom-command" ]
  then
    python manage.py "$APP_COMMAND"
  fi
  # do standard start
if [ "$APP_MODE" = "wsgi" ]
  then
  gunicorn ply.wsgi:application -b 0.0.0.0:8000
fi
if [ "$APP_MODE" = "celery" ]
  then
  celery -A ply worker -l INFO --without-heartbeat --without-gossip --without-mingle
fi