python manage.py collectstatic --no-input
export CURRENT_EVENT_PK="d1245410-08b0-457c-9439-d6b1f1345ba8"
gunicorn ply.wsgi:application -b 0.0.0.0:8000