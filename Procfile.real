web: gunicorn csv_creator.wsgi --log-file -
worker: celery -A celery_app worker -l info
