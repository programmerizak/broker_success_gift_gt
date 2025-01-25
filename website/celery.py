from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()






####NOTE TO RUN CELERY YOU DO THE FOLLOWING
# NB: For any command to be run in celery it should be added to a file tasks.py
# located inside any of your django app

# b4 running the following commands make sure your virtualenv is activated

#Start the Celery Worker(shared task/Assychronous/simultaneous):
#celery -A website worker --loglevel=info

#Start the Celery Beat Scheduler(For Periodic Task, run every 2Hours):
#celery -A website beat --loglevel=info



