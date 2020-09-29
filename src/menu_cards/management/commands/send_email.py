import logging

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management import BaseCommand
from faker import Faker

logger = logging.getLogger(__name__)

EXAMPLE_SUPER_USER = {
    "username": "admin",
    "email": "admin@gmail.com",
    "password": "adminadmin",
}

faker = Faker()
USERS_NUM = 10
SUPER_USERS_NUM = 1


class Command(
    BaseCommand,
):
    help = "Send email to users"

    def handle(self, *args, **options):
        recipients = _get_all_users()
        send_email_to_recipient(recipients)
        logger.info(f"Emails successfully sent")


def send_email_to_recipient(recipients):
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        recipients,
        fail_silently=False,
    )


def _get_all_users():
    return list(User.objects.only("email").values_list("email", flat=True))
