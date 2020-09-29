import logging

import factory
from django.core.management import BaseCommand
from django.db import transaction

from menu_cards.models import FOOD_TYPE_CHOICES, Dish
from seeder.factories.dishes import DishFactory
from seeder.factories.menus import MenuCardsFactory

logger = logging.getLogger(__name__)
NUMBER_OF_TEST_DISHES = 15
NUMBER_OF_TEST_MENU_CARDS = 5
EXAMPLE_MEAT_DISHES = [
    "Roasted Chichek Wings",
    "Spicy Herbed Chicken",
    "Sugar Rib Roast",
    "Sweet Curried Mussels",
    "Steak with Winterberry Sauce",
    "Flatbread",
    "Meatballs",
]
EXAMPLE_VEGETARIAN_DISHES = [
    "Bowl of Chocolate Tapioca Pudding",
    "Avocado Smoothie",
    "Roasted Cactus",
    "Flatbread",
    "Scrambled Eggs",
]
EXAMPLE_VEGAN_DISHES = ["Chickpea Curry", "Potato Massaman curry", "Fries"]

EXAMPLE_DISHES = EXAMPLE_VEGETARIAN_DISHES + EXAMPLE_MEAT_DISHES + EXAMPLE_VEGAN_DISHES


class Command(
    BaseCommand,
):
    help = "Populate DB with test data"

    def handle(self, *args, **options):
        create_dishes()
        create_menu_cards()
        logger.info("Database successfully filled with mocks")


def create_dishes():
    meat = [DishFactory.create(name=meat_dish) for meat_dish in EXAMPLE_MEAT_DISHES]
    vegetarian = [
        DishFactory.create(name=vegetarian_dish)
        for vegetarian_dish in EXAMPLE_VEGETARIAN_DISHES
    ]
    vegan = [DishFactory.create(name=vegan_dish) for vegan_dish in EXAMPLE_VEGAN_DISHES]

    # meat = DishFactory.create_batch(len(EXAMPLE_MEAT_DISHES))
    # vegetarian = DishFactory.create_batch(len(EXAMPLE_VEGETARIAN_DISHES))
    # vegan = DishFactory.create_batch(len(EXAMPLE_VEGAN_DISHES))

    logger.info("Created dishes:")
    assign_dish_fields(meat, EXAMPLE_MEAT_DISHES, FOOD_TYPE_CHOICES.meat)
    assign_dish_fields(
        vegetarian, EXAMPLE_VEGETARIAN_DISHES, FOOD_TYPE_CHOICES.vegetarian
    )
    assign_dish_fields(vegan, EXAMPLE_VEGAN_DISHES, FOOD_TYPE_CHOICES.vegan)

    logger.info("meat: %s" % meat)
    logger.info("vegetarian: %s" % vegetarian)
    logger.info("vegan: %s" % vegan)
    return meat + vegetarian + vegan


def create_menu_cards():
    menu_cards = MenuCardsFactory.create_batch(NUMBER_OF_TEST_MENU_CARDS)

    meat_dishes = Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.meat)
    vegetarian_dishes = Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.vegetarian)
    vegan_dishes = Dish.objects.filter(food_type=FOOD_TYPE_CHOICES.vegan)

    assign_dishes_to_cards(meat_dishes, menu_cards[0])
    assign_dishes_to_cards(vegetarian_dishes, menu_cards[1])
    assign_dishes_to_cards(vegan_dishes, menu_cards[2])

    return menu_cards


@transaction.atomic
def assign_dishes_to_cards(dishes, card):
    for dish in dishes:
        dish.menu_card = card
        dish.save()


@transaction.atomic
def assign_dish_fields(dishes, food_names, food_type):
    assert len(dishes) == len(food_names)
    for dish, name in zip(dishes, food_names):
        # dish.name = name
        dish.food_type = food_type
        dish.save()
