# project-receipt

celery -A PhotoProject.celery worker --loglevel=INFO
redis-server
python manage.py runserver
celery -A PhotoProject beat -l INFO
