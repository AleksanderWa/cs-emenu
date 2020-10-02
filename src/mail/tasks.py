import logging

from celery import shared_task
from django.core.management import call_command
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_emails():
    current_time = timezone.now()
    logger.info(f"Send emails task initiated : {current_time}")
    call_command("send_emails")
    return True
