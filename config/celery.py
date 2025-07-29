# api/config/celery.py ← 있어야 함!
from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("royalty-api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
