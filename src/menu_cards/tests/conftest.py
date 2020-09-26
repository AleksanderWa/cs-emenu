import pytest
from django.test import Client
from model_bakery import baker

from menu_cards.models import Dish, MenuCard, FOOD_TYPE_CHOICES
from seeder.management.commands.seed_db import (
    EXAMPLE_MEAT_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
    EXAMPLE_VEGAN_DISHES,
)


def client():
    return Client()


@pytest.fixture
def meat_dishes(menu_card):
    return [
        baker.make(
            Dish,
            name=dish,
            food_type=FOOD_TYPE_CHOICES.meat,
            menu_card=menu_card,
        )
        for dish in EXAMPLE_MEAT_DISHES
    ]


@pytest.fixture
def vegetarian_menu():
    return [
        baker.make(
            Dish,
            name=dish,
            food_type=FOOD_TYPE_CHOICES.vegetarian,
            menu_card=menu_card,
        )
        for dish in EXAMPLE_VEGETARIAN_DISHES
    ]


@pytest.fixture
def vegan_menu():
    # menu_card = baker.make(MenuCard, name="Plant based card")
    # dishes = [
    #     baker.make(Dish, name=dish, food_type=FOOD_TYPE_CHOICES.vegan, menu_card=menu_card)
    #     for dish in EXAMPLE_VEGAN_DISHES
    # ]
    # menu_card = create_menu_card(dict(name="Vegan Dishes"), EXAMPLE_VEGAN_DISHES)
    menu_card = create_menu_card(
        dict(name='Vegan card', description='for carrots lovers'),
        dict(food_type=FOOD_TYPE_CHOICES.vegan),
        EXAMPLE_VEGAN_DISHES
    )
    return menu_card


@pytest.fixture
def menu_card():
    return baker.make(MenuCard, name='Bon Appetit !')


def create_menu_card(menu_attr=None, dish_attrs=None, dishes=None):
    menu_attr = menu_attr or {}
    dish_attrs = dish_attrs or {}
    dishes = dishes or []

    menu_card = baker.make(MenuCard, menu_attr)
    for dish in dishes:
        baker.make(Dish, name=dish, menu_card=menu_card, **dish_attrs)
    return baker.make(MenuCard, **menu_attr)


