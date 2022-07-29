from __future__ import absolute_import, unicode_literals
from datetime import time
import os
from celery import Celery
from project import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')

#CELERY BEAT SETTINGS

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')