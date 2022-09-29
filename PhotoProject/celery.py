from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PhotoProject.settings")

app = Celery("project_celery")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "send_email_to_project_users_sunday": {
        "task": "photoproject.tasks.send_email_to_project_users",
        # "schedule": crontab(hour=22, minute=50),
        "schedule": crontab(hour=21, minute=0, day_of_week="sun"),
        # "args": (arg1, arg2)
    }
}


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
