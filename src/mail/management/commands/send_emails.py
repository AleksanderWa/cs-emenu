import logging

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import Q
from django.utils import timezone
from faker import Faker

from menu_cards.models import Dish, MenuCard

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
        email_content = get_cards_and_dishes_for_yesterday()
        send_email_to_recipient(recipients, email_content)
        logger.info(f"Emails successfully sent")


def send_email_to_recipient(recipients, email_content):
    send_mail(
        "Dishes and menu cards added or modified yesterday: ",
        f"{email_content}",
        "from@example.com",
        recipients,
        fail_silently=False,
    )


def _get_all_users():
    return list(User.objects.only("email").values_list("email", flat=True))


def get_cards_and_dishes_for_yesterday():
    yesterday = timezone.datetime.today() - timezone.timedelta(days=1)
    modified_filter = _get_modified_on_date_query(yesterday)
    created_filter = _get_create_on_date_query(yesterday)

    modified_dishes = _get_modified_dishes(modified_filter)
    created_dishes = _get_created_dishes(created_filter)

    modified_menus = _get_modified_menu_cards(modified_filter)
    created_menus = _get_created_menu_cards(created_filter)

    return (modified_dishes, created_dishes) + (modified_menus, created_menus)


def _get_modified_dishes(modified_filter):
    return Dish.objects.filter(modified_filter)


def _get_created_dishes(created_filter):
    return Dish.objects.filter(created_filter)


def _get_modified_menu_cards(modified_filter):
    return MenuCard.objects.filter(modified_filter)


def _get_created_menu_cards(created_filter):
    return MenuCard.objects.filter(created_filter)


def _get_modified_on_date_query(date):
    return (
        Q(modified__year=date.year)
        & Q(modified__month=date.month)
        & Q(modified__day=date.day)
    )


def _get_create_on_date_query(date):
    return (
        Q(created__year=date.year)
        & Q(created__month=date.month)
        & Q(created__day=date.day)
    )
