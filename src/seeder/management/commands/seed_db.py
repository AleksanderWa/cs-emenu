import logging
import factory
from django.db import transaction

from menu_cards.models import Dish, FOOD_TYPE_CHOICES
from django.core.management import BaseCommand
from seeder.factories.dishes import DishFactory
from seeder.factories.menus import MenuCardsFactory

logger = logging.getLogger(__name__)
print(f"logger name : {logger}")
NUMBER_OF_TEST_DISHES = 15
NUMBER_OF_TEST_MENU_CARDS = 5
EXAMPLE_MEAT_DISHES = [
    'Roasted Cactus',
    'Spicy Herbed Chicken',
    'Sugar Rib Roast',
    'Sweet Curried Mussels',
    'Steak with Winterberry Sauce',
    'Flatbread',
    'Meatballs',
]
EXAMPLE_VEGETARIAN_DISHES = [
    'Bowl of Chocolate Tapioca Pudding',
    'Avocado Smoothie',
    'Roasted Cactus',
    'Flatbread',
    'Scrambled Eggs',
]
EXAMPLE_VEGAN_DISHES = ['Chickpea Curry', 'Potato Massaman curry', 'Fries']

EXAMPLE_DISHES = (
    EXAMPLE_VEGETARIAN_DISHES + EXAMPLE_MEAT_DISHES + EXAMPLE_VEGAN_DISHES
)


class Command(
    BaseCommand,
):
    help = "Populate DB with test data"

    def handle(self, *args, **options):
        create_dishes()
        create_menu_cards()
        logger.info('Database successfully filled with mocks')


def create_dishes():
    meat = DishFactory.create_batch(len(EXAMPLE_MEAT_DISHES))
    vegetarian = DishFactory.create_batch(len(EXAMPLE_VEGETARIAN_DISHES))
    vegan = DishFactory.create_batch(len(EXAMPLE_VEGAN_DISHES))

    logger.info('Created dishes:')
    assign_dish_fields(meat, EXAMPLE_MEAT_DISHES, FOOD_TYPE_CHOICES.meat)
    assign_dish_fields(
        vegetarian, EXAMPLE_VEGETARIAN_DISHES, FOOD_TYPE_CHOICES.vegetarian
    )
    assign_dish_fields(vegan, EXAMPLE_VEGAN_DISHES, FOOD_TYPE_CHOICES.vegan)

    logger.info('meat: %s' % meat)
    logger.info('vegetarian: %s' % vegetarian)
    logger.info('vegan: %s' % vegan)
    return meat + vegetarian + vegan


def create_menu_cards():
    meat_dishes = factory.Iterator(
        Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.meat)
    )
    meat_card = MenuCardsFactory(dish=meat_dishes)

    vegetarian_dishes = factory.Iterator(
        Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.vegetarian)
    )
    vegetarian_card = MenuCardsFactory(dish=vegetarian_dishes)

    vegan_dishes = factory.Iterator(
        Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.vegan)
    )
    vegan_card = MenuCardsFactory(dish=vegan_dishes)

    return meat_card, vegetarian_card, vegan_card


@transaction.atomic
def assign_dish_fields(dishes, food_names, food_type):
    assert len(dishes) == len(food_names)
    for dish, name in zip(dishes, food_names):
        dish.name = name
        dish.food_type = food_type
        dish.save()
