import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx_ua_parser.settings')

app = Celery('olx_ua_parser')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
