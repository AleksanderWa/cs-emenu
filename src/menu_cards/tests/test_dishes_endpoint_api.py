from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from menu_cards.models import Dish, MenuCard, FOOD_TYPE_CHOICES
from model_bakery import baker
from menu_cards.tests.conftest import client
from seeder.management.commands.seed_db import (
    EXAMPLE_MEAT_DISHES,
    EXAMPLE_VEGAN_DISHES,
)


class DishesEndpointTest(TestCase):
    def setUp(self):
        """Setup for tests to seed db with a test data"""

        # for dish in EXAMPLE_MEAT_DISHES:
        #     baker.make(Dish, name=dish, food_type=FOOD_TYPE_CHOICES.meat)
        #
        # for dish in EXAMPLE_MEAT_DISHES:
        #     baker.make(Dish, name=dish, food_type=FOOD_TYPE_CHOICES.meat)
        #
        # self.Dish1 = baker.make(Dish, name='', unidecode_name='testuser')
        # self.Dish2 = baker.make(
        #     Dish, full_name="Test_user2", unidecode_name='testuser2'
        # )
        # self.article1 = mommy.make(Article, Dish=self.Dish1, title='test title',
        #                            text='asd third')
        # self.article2 = mommy.make(Article, Dish=self.Dish2, title='test', text='asd test')

    def test_api_list_all_dishes(self, client):
        response = client().get(reverse('dishes-list'))
        expected_result = {'asd': 2, 'third': 1, 'test': 1}
        breakpoint()
        self.assertEqual(response.data, expected_result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
