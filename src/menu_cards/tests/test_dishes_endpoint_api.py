import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from menu_cards.models import Dish, MenuCard, FOOD_TYPE_CHOICES
from model_bakery import baker
from menu_cards.tests.conftest import (
    client,
    create_menu_card,
    valid_data_for_dish_creation,
)
from seeder.management.commands.seed_db import (
    EXAMPLE_MEAT_DISHES,
    EXAMPLE_VEGAN_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
)

LIST_URL = 'dishes-list'
DETAIL_URL = 'dishes-detail'


class DishesEndpointTest(TestCase):
    def setUp(self):
        """Setup for tests to seed db with a test data"""

        vegan_card = create_menu_card(
            dict(name='Vegan card', description='for carrots lovers'),
            dict(food_type=FOOD_TYPE_CHOICES.vegan),
            EXAMPLE_VEGAN_DISHES,
        )
        vegetarian_card = create_menu_card(
            dict(name='Vegetarian card', description='Non meat eaters'),
            dict(food_type=FOOD_TYPE_CHOICES.vegetarian),
            EXAMPLE_VEGETARIAN_DISHES,
        )

    def test_dishes__get_list_all_dishes(self):
        url = reverse(LIST_URL)
        response = client().get(url)
        for item in response.data:
            self.assertIn(
                item.get('name'),
                EXAMPLE_VEGETARIAN_DISHES + EXAMPLE_VEGAN_DISHES,
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dishes__get_shows_name_of_menu_card(self):
        url = reverse(LIST_URL)
        response = client().get(url)

        assert all([item.get('menu_card') for item in response.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dishes__retrieve_single_dish(self):
        dish_from_db = Dish.objects.only('id').first()
        url = reverse('dishes-detail', args=(dish_from_db.id,))
        response = client().get(url)
        self.assertEqual(dish_from_db.id, response.data.get('id'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dishes__single_dish_creation(self):
        url = reverse(LIST_URL)
        response = client().post(
            url, data=valid_data_for_dish_creation(), format='json'
        )
        created_dish = response.data
        dish_exists = Dish.objects.filter(id=created_dish.get('id')).exists()

        assert dish_exists
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
