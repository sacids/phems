from __future__ import absolute_import ,unicode_literals
from celery import Celery
from django.conf import settings
import os
# SETTINGS
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone = 'Africa/Nairobi')
app.config_from_object(settings,namespace='CELERY')
# CELERY BEAT Settings
app.conf.beat_schedule = {
}
app.autodiscover_tasks()
#task setting
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')