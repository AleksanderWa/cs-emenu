import freezegun as freezegun
import pytest
from django.utils import timezone

from mail.management.commands.send_email import (
    _get_create_on_date_query, _get_created_dishes, _get_created_menu_cards,
    _get_modified_dishes, _get_modified_menu_cards,
    _get_modified_on_date_query, get_cards_and_dishes_for_yesterday)
from menu_cards.models import Dish, MenuCard
from menu_cards.tests.conftest import (meat_dish, meat_menu, vegan_menu,
                                       vegetarian_dish)

MENU_LIST_URL = "menus-list"
MENU_DETAIL_URL = "menus-detail"

pytestmark = pytest.mark.django_db
TIMESTAMP = timezone.datetime(2020, 1, 1, 17, 20, 59, tzinfo=timezone.utc)


@freezegun.freeze_time(timezone.now())
def test_get_yesterdays_modified_and_created_dishes(meat_dish, vegan_menu):
    yesterday = timezone.datetime.today() - timezone.timedelta(days=1, hours=5)
    with freezegun.freeze_time(timezone.now() - timezone.timedelta(days=1)):
        dish = Dish.objects.all().first()
        dish.name = "Alter name"
        dish.save()
    modified_filter = _get_modified_on_date_query(yesterday)
    created_filter = _get_create_on_date_query(yesterday)

    modified_dishes = _get_modified_dishes(modified_filter)
    created_dishes = _get_created_dishes(created_filter)
    meat_dish.refresh_from_db()
    assert Dish.objects.all().count() == 4
    assert len(modified_dishes | created_dishes) == 1
    assert modified_dishes[0] == meat_dish


@freezegun.freeze_time(timezone.now())
def test_get_yesterdays_modified_and_created_menus(meat_menu, vegan_menu):
    yesterday = timezone.datetime.today() - timezone.timedelta(days=1, hours=5)
    with freezegun.freeze_time(timezone.now() - timezone.timedelta(days=1)):
        menu = MenuCard.objects.get(name=meat_menu.name)
        menu.name = "Alter name"
        menu.save()
    modified_filter = _get_modified_on_date_query(yesterday)
    created_filter = _get_create_on_date_query(yesterday)

    modified_menus = _get_modified_menu_cards(modified_filter)
    created_menus = _get_created_menu_cards(created_filter)
    meat_menu.refresh_from_db()
    assert MenuCard.objects.all().count() == 2
    assert len(modified_menus | created_menus) == 1
    assert modified_menus[0] == meat_menu
