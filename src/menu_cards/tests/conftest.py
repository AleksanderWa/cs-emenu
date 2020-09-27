import pytest
from django.test import Client
from model_bakery import baker

from menu_cards.models import Dish, MenuCard, FOOD_TYPE_CHOICES
from seeder.management.commands.seed_db import (
    EXAMPLE_VEGAN_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
    EXAMPLE_MEAT_DISHES,
)


def client():
    return Client()


@pytest.fixture
def meat_menu():
    return create_menu_card(
        dict(name='Protein', description='meat and more meat'),
        dict(food_type=FOOD_TYPE_CHOICES.meat),
        EXAMPLE_MEAT_DISHES,
    )


@pytest.fixture
def vegan_menu():
    return create_menu_card(
        dict(name='Vegan card', description='for carrots lovers'),
        dict(food_type=FOOD_TYPE_CHOICES.vegan),
        EXAMPLE_VEGAN_DISHES,
    )


@pytest.fixture
def vegetarian_menu():
    return create_menu_card(
        dict(name='Cheese card', description='!MEAT'),
        dict(food_type=FOOD_TYPE_CHOICES.vegetarian),
        EXAMPLE_VEGETARIAN_DISHES,
    )


def create_menu_card(menu_attr=None, dish_attrs=None, dishes_names=None):
    menu_attr = menu_attr or {}
    dish_attrs = dish_attrs or {}
    dishes_names = dishes_names or []
    menu_card = baker.make(MenuCard, **menu_attr)
    for dish in dishes_names:
        baker.make(Dish, name=dish, menu_card=menu_card, **dish_attrs)
    return menu_card


def valid_data_for_dish_creation():
    return {
        "name": "Good Food",
        "description": "100% beef",
        "price": "100.12",
        "prep_time": "00:15:12",
        "food_type": "10",
        "menu_card": "1",
    }


def invalid_data_for_dish_creation():
    return {
        "name": "Good Food",
        "description": "100% beef",
        "food_type": "10",
    }


def valid_data_for_menu_creation():
    return {
        "name": "Best Menu!",
        "description": "Funny description goes here",
        "dishes": [
            {
                "name": "Good Food",
                "description": "100% beef",
                "price": "100.12",
                "prep_time": "00:15:12",
                "food_type": "10",
            },
        ],
    }


def invalid_data_for_menu_creation():
    return {
        "bad_field": "sad menu",
        "description": "It ain't gonna work",
    }
