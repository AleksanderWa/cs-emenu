from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import connection, reset_queries
from django.test import TestCase

from menu_cards.models import Dish, MenuCard
from seeder.management.commands.create_users import (EXAMPLE_SUPER_USER,
                                                     SUPER_USERS_NUM,
                                                     USERS_NUM)
from seeder.management.commands.seed_db import EXAMPLE_DISHES


class SeedDBCommandTest(TestCase):
    logger = "seeder.management.commands.seed_db"

    def test_seed_db_command_successful_run(self):
        with self.assertLogs(self.logger, level="INFO") as caplog:
            call_command("seed_db")
            self.assertIn("Created dishes:", caplog.output[0])
            self.assertIn("Database successfully filled with mocks", caplog.output[-1])

    def test_mocked_dishes_have_correct_names(self):
        with self.assertLogs(self.logger, level="INFO") as caplog:
            call_command("seed_db")
            dishes_from_db = Dish.objects.only("name").values_list("name", flat=True)
            self.assertSetEqual(set(dishes_from_db), set(EXAMPLE_DISHES))

    def test_mocked_cards_have_dishes(self):
        empty_cards = 2
        filled_cards = 3
        call_command("seed_db")
        filled_cards_from_db = (
            MenuCard.objects.filter(dishes__isnull=False).distinct().count()
        )
        empty_cards_from_db = (
            MenuCard.objects.filter(dishes__isnull=True).distinct().count()
        )
        assert filled_cards_from_db == filled_cards
        assert empty_cards_from_db == empty_cards


class CreateUsersCommandTest(TestCase):
    logger = "seeder.management.commands.create_users"

    def test_seed_db_command_successful_run(self):
        with self.assertLogs(self.logger, level="INFO") as caplog:
            call_command("create_users")
            assert User.objects.all().count() == USERS_NUM + SUPER_USERS_NUM
            assert User.objects.filter(
                email=EXAMPLE_SUPER_USER["email"], is_superuser=True
            ).exists()
            self.assertIn("Users successfully created!", caplog.output[-1])
