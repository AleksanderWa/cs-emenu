import json

import freezegun as freezegun
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from menu_cards.models import MenuCard
from seeder.management.commands.seed_db import (
    EXAMPLE_VEGAN_DISHES,
    EXAMPLE_VEGETARIAN_DISHES,
)

MENU_LIST_URL = 'menus-list'
MENU_DETAIL_URL = 'menus-detail'

pytestmark = pytest.mark.django_db
TIMESTAMP = timezone.datetime(2020, 1, 1, 17, 20, 59, tzinfo=timezone.utc)


def test_menus__list_all_menus(superadmin_client, vegan_menu):
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.get(url)
    for item in response.data:
        assert item.get('name') == vegan_menu.name
    assert response.status_code == status.HTTP_200_OK


def test_menus__get_includes_dishes(
    superadmin_client, vegan_menu, vegetarian_menu
):
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.get(url)
    assert all(
        [
            dish.get('name')
            in (EXAMPLE_VEGETARIAN_DISHES + EXAMPLE_VEGAN_DISHES)
            for menu in response.data
            for dish in menu.get('dishes')
        ]
    )
    assert response.status_code == status.HTTP_200_OK


def test_menus__retrieve_single_menu(superadmin_client, meat_menu):
    menu_from_db = MenuCard.objects.only('id').first()
    url = reverse(MENU_DETAIL_URL, args=(menu_from_db.id,))
    response = superadmin_client.get(url)
    assert menu_from_db.id == response.data.get('id')
    assert response.status_code == status.HTTP_200_OK


def test_menus__single_menu_creation(
    superadmin_client, valid_data_for_menu_creation
):
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.post(
        url,
        data=json.dumps(valid_data_for_menu_creation),
        content_type='application/json',
    )
    created_menu = response.data
    menu_exists = MenuCard.objects.filter(id=created_menu.get('id')).exists()
    assert menu_exists
    assert response.status_code == status.HTTP_201_CREATED


def test_dishes__returns_400_when_duplicated_dish_in_card(
    superadmin_client,
    valid_data_for_dish_creation,
    valid_data_for_menu_creation,
):
    error_msg = "List contains duplicated dish names"
    dishes = [valid_data_for_dish_creation for _ in range(3)]
    valid_data_for_menu_creation['dishes'] = dishes
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.post(
        url, data=valid_data_for_menu_creation, format='json'
    )
    assert error_msg in response.data['dishes'][0]
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_menus__dish_creation_error_on_wrong_data(
    superadmin_client, invalid_data_for_menu_creation
):
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.post(
        url, data=invalid_data_for_menu_creation, format='json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


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
    superadmin_client,
    field,
    ordered,
    reverse_ordered,
    vegan_menu,
    vegetarian_menu,
    meat_menu,
):

    url = reverse(MENU_LIST_URL)
    response = superadmin_client.get(url, {'ordering': field})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), ordered)
        ]
    )
    response = superadmin_client.get(url, {'ordering': f"-{field}"})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), reverse_ordered)
        ]
    )


def test_menus__annotate_num_dishes(superadmin_client, vegan_menu):
    url = reverse(MENU_LIST_URL)
    response = superadmin_client.get(url)
    assert response.data[0].get('dishes_num') == vegan_menu.dishes.count()


@freezegun.freeze_time(TIMESTAMP)
def test_menus__patch_updates_timestamps(
    superadmin_client, vegan_menu, valid_data_to_update_menu
):

    url = reverse(MENU_DETAIL_URL, args=(vegan_menu.id,))
    response = superadmin_client.patch(
        url,
        data=json.dumps(valid_data_to_update_menu),
        content_type='application/json',
    )

    assert MenuCard.objects.first().modified == TIMESTAMP
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'field, expected_card',
    [
        (
            'created',
            'Cheese card',
        ),
        (
            'modified',
            'Vegan card',
        ),
    ],
)
def test_menus__filter_by_field(
    superadmin_client,
    field,
    expected_card,
    vegan_menu,
    vegetarian_menu,
    meat_menu,
):
    url = reverse(MENU_LIST_URL)
    filter_value = MenuCard.objects.filter(name=expected_card).values_list(
        field, flat=True
    )[0]
    response = superadmin_client.get(url, {field: filter_value})
    assert response.data[0].get('name') == expected_card
