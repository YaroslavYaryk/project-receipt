# project-receipt

celery -A PhotoProject.celery worker --loglevel=error
redis-server
python manage.py runserver
