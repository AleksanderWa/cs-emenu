import pytest
pytestmark = pytest.mark.django_db


def test_meat_is_not_vegetarian(meat_dish):
    assert not meat_dish.is_vegetarian