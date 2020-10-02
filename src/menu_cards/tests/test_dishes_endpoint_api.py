import freezegun
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.utils import json

from menu_cards.models import FOOD_TYPE_CHOICES, Dish, DishPhoto
from menu_cards.tests.test_menu_endpoint_api import TIMESTAMP

DISHES_URL = "dishes"
DISHES_LIST_URL = f"{DISHES_URL}-list"
DISHES_DETAIL_URL = f"{DISHES_URL}-detail"

pytestmark = pytest.mark.django_db


def test_dishes__list_all_dishes(superadmin_client, vegan_menu):
    url = reverse(DISHES_LIST_URL)
    response = superadmin_client.get(url)
    db_names = vegan_menu.dishes.only("name").values_list("name", flat=True)
    for item in response.data:
        assert item.get("name") in db_names
    assert response.status_code == status.HTTP_200_OK


def test_dishes__get_shows_name_of_menu_card(superadmin_client, vegetarian_menu):
    url = reverse(DISHES_LIST_URL)
    response = superadmin_client.get(url)

    assert all([item.get("menu_card") for item in response.data])
    assert response.status_code == status.HTTP_200_OK


def test_dishes__retrieve_single_dish(superadmin_client, vegetarian_dish):
    dish_from_db = Dish.objects.only("id").first()
    url = reverse(DISHES_DETAIL_URL, args=(dish_from_db.id,))
    response = superadmin_client.get(url)
    assert dish_from_db.id == response.data.get("id")
    assert response.status_code == status.HTTP_200_OK


def test_dishes__single_dish_creation(superadmin_client, valid_data_for_dish_creation):
    url = reverse(DISHES_LIST_URL)
    response = superadmin_client.post(
        url, data=valid_data_for_dish_creation, format="json"
    )
    created_dish = response.data
    dish_exists = Dish.objects.filter(id=created_dish.get("id")).exists()
    assert dish_exists
    assert response.status_code == status.HTTP_201_CREATED


def test_dishes__dish_creation_error_on_wrong_data(
    superadmin_client, invalid_data_for_dish_creation
):
    url = reverse(DISHES_LIST_URL)
    response = superadmin_client.post(
        url, data=invalid_data_for_dish_creation, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "field, values, ordered, reverse_ordered",
    [
        (
            "price",
            [1.01, 5.01, 2.01],
            [1.01, 2.01, 5.01],
            [5.01, 2.01, 1.01],
        ),
        (
            "food_type",
            [
                FOOD_TYPE_CHOICES.meat,
                FOOD_TYPE_CHOICES.vegan,
                FOOD_TYPE_CHOICES.meat,
            ],
            [
                FOOD_TYPE_CHOICES.meat,
                FOOD_TYPE_CHOICES.meat,
                FOOD_TYPE_CHOICES.vegan,
            ],
            [
                FOOD_TYPE_CHOICES.vegan,
                FOOD_TYPE_CHOICES.meat,
                FOOD_TYPE_CHOICES.meat,
            ],
        ),
    ],
)
def test_dishes__are_ordered_by_field(
    superadmin_client, field, values, ordered, reverse_ordered
):
    for value in values:
        baker.make(Dish, **{field: value})

    url = reverse(DISHES_LIST_URL)
    response = superadmin_client.get(url, {"ordering": field})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), ordered)
        ]
    )
    response = superadmin_client.get(url, {"ordering": f"-{field}"})
    assert all(
        [
            str(item[field]) == str(expected)
            for item, expected in zip(response.json(), reverse_ordered)
        ]
    )


@freezegun.freeze_time(TIMESTAMP)
def test_dishes__patch_updates_timestamps(
    superadmin_client, meat_dish, valid_data_to_update_dish
):

    url = reverse(DISHES_DETAIL_URL, args=(meat_dish.id,))
    response = superadmin_client.patch(
        url,
        data=json.dumps(valid_data_to_update_dish),
        content_type="application/json",
    )

    assert Dish.objects.first().modified == TIMESTAMP
    assert response.status_code == status.HTTP_200_OK


def test_dishes__added_photo_to_dish(superadmin_client, meat_dish, photo):
    url = reverse(f"{DISHES_URL}-photo", args=(meat_dish.id,))

    response = superadmin_client.post(
        url,
        data={"image": photo},
    )
    assert Dish.objects.first().photos
    assert response.status_code == status.HTTP_201_CREATED


def test_dishes__photo_included_in_response(superadmin_client, meat_dish):
    url = reverse(f"{DISHES_DETAIL_URL}", args=(meat_dish.id,))
    photo = baker.make(DishPhoto, dish=meat_dish)
    response = superadmin_client.get(
        url,
    )
    assert response.data['photos'][0]['id'] == photo.id
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "method, expected_response",
    [
        ("get", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("post", status.HTTP_201_CREATED),
        ("patch", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("delete", status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
)
def test_dishes__add_photo_accepts_only_post_method(
    superadmin_client, method, expected_response, meat_dish, photo
):
    url = reverse(f"{DISHES_URL}-photo", args=(meat_dish.id,))
    http_method = getattr(superadmin_client, method)
    response = http_method(
        url,
        data={"image": photo},
    )
    assert response.status_code == expected_response
