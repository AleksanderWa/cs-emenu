import factory
from menu_cards.models import Dish
from django.core.management import BaseCommand
from seeder.factories.dishes import DishFactory
from seeder.factories.menus import MenuCardsFactory

NUMBER_OF_TEST_DISHES = 15
NUMBER_OF_TEST_MENU_CARDS = 5


class Command(
    BaseCommand,
):
    help = "Populate DB with test data"

    def handle(self, *args, **options):
        create_dishes()
        create_menu_cards()


def create_dishes(amount=NUMBER_OF_TEST_DISHES):
    return DishFactory.create_batch(amount)


def create_menu_cards(amount=NUMBER_OF_TEST_MENU_CARDS):
    dishes = factory.Iterator(Dish.objects.all())
    return MenuCardsFactory.create_batch(amount, dish=dishes)
