import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eMenu.settings")

app = Celery("eMenu")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
