from io import StringIO

import pytest
from django.db import connection, reset_queries
from django.core.management import call_command
from django.test import TestCase
from menu_cards.models import Dish, MenuCard
from seeder.management.commands.seed_db import (
    EXAMPLE_DISHES,
    EXAMPLE_MEAT_DISHES,
    EXAMPLE_VEGAN_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
)

logger = 'seeder.management.commands.seed_db'


class SeedDBCommandTest(TestCase):
    def test_seed_db_command_successful_run(self):
        with self.assertLogs(logger, level='INFO') as caplog:
            call_command('seed_db')
            self.assertIn('Created dishes:', caplog.output[0])
            self.assertIn(
                'Database successfully filled with mocks', caplog.output[-1]
            )
            print(len(connection.queries))

    def test_mocked_dishes_have_correct_names(self):
        with self.assertLogs(logger, level='INFO') as caplog:
            call_command('seed_db')
            dishes_from_db = Dish.objects.only('name').values_list(
                'name', flat=True
            )
            self.assertSetEqual(set(dishes_from_db), set(EXAMPLE_DISHES))

    def test_mocked_cards_have_dishes(self):
        empty_cards = 2
        filled_cards = 3
        call_command('seed_db')
        filled_cards_from_db = (
            MenuCard.objects.filter(dishes__isnull=False).distinct().count()
        )
        empty_cards_from_db = (
            MenuCard.objects.filter(dishes__isnull=True).distinct().count()
        )
        assert filled_cards_from_db == filled_cards
        assert empty_cards_from_db == empty_cards

    # @pytest.mark.parametrize("card, dishes", [("meat", EXAMPLE_MEAT_DISHES),
    #                                           ("vegetarian", EXAMPLE_VEGETARIAN_DISHES),
    #                                           ("vegan", EXAMPLE_VEGAN_DISHES)])
    # def test_mocked_cards_contain_dishes(self, card, dishes):
    #     call_command('seed_db')
    #     cards_from_db = MenuCard.objects.all()
    #
    #     self.assertSetEqual(set(dishes_from_db), set(EXAMPLE_DISHES))
