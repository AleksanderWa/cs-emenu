from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from menu_cards.models import Dish, MenuCard
from seeder.management.commands.seed_db import EXAMPLE_DISHES

logger = 'seeder.management.commands.seed_db'


class SeedDBCommandTest(TestCase):
    def test_seed_db_command_successful_run(self):
        with self.assertLogs(logger, level='INFO') as caplog:
            out = StringIO()
            call_command('seed_db', stdout=out)
            self.assertIn('Created dishes:', caplog.output[0])
            self.assertIn(
                'Database successfully filled with mocks', caplog.output[-1]
            )

    def test_db_has_correct_data(self):
        with self.assertLogs(logger, level='INFO') as caplog:
            call_command('seed_db')
            dishes_from_db = Dish.objects.only('name').values_list(
                'name', flat=True
            )
            self.assertSetEqual(set(dishes_from_db), set(EXAMPLE_DISHES))
