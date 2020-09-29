import logging

from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command
from faker import Faker

from seeder.factories.users import UserFactory

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
    help = "Create test users"

    def handle(self, *args, **options):
        # call_command("createsuperuser", **EXAMPLE_SUPER_USER)
        create_users()
        create_superuser()
        logger.info("Users successfully created!")


def create_users():
    users = [UserFactory.create(**_generate_data()) for _ in range(USERS_NUM)]
    logger.info(f"Created : {users}")
    return users


def create_superuser():
    username = EXAMPLE_SUPER_USER["username"]
    password = EXAMPLE_SUPER_USER["password"]
    email = EXAMPLE_SUPER_USER["email"]
    superuser = User.objects.create_superuser(
        username=username, email=email, password=password
    )
    logger.info(f"Created superuser: {superuser}")


def _generate_data():
    return {
        "username": faker.name(),
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
    }
