import json

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from menu_cards.models import Dish, MenuCard, FOOD_TYPE_CHOICES
from model_bakery import baker
from menu_cards.tests.conftest import (
    client,
    create_menu_card,
    valid_data_for_menu_creation,
    invalid_data_for_menu_creation,
)
from seeder.management.commands.seed_db import (
    EXAMPLE_VEGAN_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
)

LIST_URL = 'menus-list'
DETAIL_URL = 'menus-detail'


class MenuEndpointTest(TestCase):
    card_names = ('Vegan card', 'Vegetarian card')

    def setUp(self):
        """Setup for tests to seed db with a test data"""

        vegan_card = create_menu_card(
            dict(name=self.card_names[0], description='for carrots lovers'),
            dict(food_type=FOOD_TYPE_CHOICES.vegan),
            EXAMPLE_VEGAN_DISHES,
        )
        vegetarian_card = create_menu_card(
            dict(name=self.card_names[1], description='Non meat eaters'),
            dict(food_type=FOOD_TYPE_CHOICES.vegetarian),
            EXAMPLE_VEGETARIAN_DISHES,
        )

    def test_menus__list_all_menus(self):
        url = reverse(LIST_URL)
        response = client().get(url)
        for item in response.data:
            self.assertIn(
                item.get('name'),
                self.card_names,
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menus__get_includes_dishes(self):
        url = reverse(LIST_URL)
        response = client().get(url)
        for menu in response.data:
            for dish in menu.get('dishes'):
                self.assertIn(
                    dish.get('name'),
                    EXAMPLE_VEGETARIAN_DISHES + EXAMPLE_VEGAN_DISHES,
                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menus__retrieve_single_menu(self):
        menu_from_db = MenuCard.objects.only('id').first()
        url = reverse(DETAIL_URL, args=(menu_from_db.id,))
        response = client().get(url)
        self.assertEqual(menu_from_db.id, response.data.get('id'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menus__single_menu_creation(self):
        url = reverse('menus-list')
        menu = valid_data_for_menu_creation()

        response = client().post(
            url, data=json.dumps(menu), content_type='application/json'
        )
        created_menu = response.data
        menu_exists = MenuCard.objects.filter(
            id=created_menu.get('id')
        ).exists()

        assert menu_exists
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_menus__dish_creation_error_on_wrong_data(self):
        url = reverse(LIST_URL)
        response = client().post(
            url, data=invalid_data_for_menu_creation(), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'field, ordered, reverse_ordered',
    [
        (
            'name',
            ['Cheese card', 'Protein', 'Vegan card'],
            ['Vegan card', 'Protein', 'Cheese card'],
        ),
        (
            'dishes_num',
            [3, 5, 7],
            [7, 5, 3],
        ),
    ],
)
def test_menus__order_by_field(
    client,
    field,
    ordered,
    reverse_ordered,
    vegan_menu,
    vegetarian_menu,
    meat_menu,
):

    url = reverse(LIST_URL)
    response = client.get(url, {'ordering': field})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), ordered)
        ]
    )
    response = client.get(url, {'ordering': f"-{field}"})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), reverse_ordered)
        ]
    )


@pytest.mark.django_db
def test_menus__annotate_num_dishes(client, vegan_menu):
    url = reverse(LIST_URL)
    response = client.get(url)
    assert response.data[0].get('dishes_num') == vegan_menu.dishes.count()
