import factory
from random import randint

from django.utils import timezone

from menu_cards.models import Dish, FOOD_TYPE_CHOICES
from factory import (
    django,
    fuzzy,
)


class DishFactory(django.DjangoModelFactory):
    food_type = FOOD_TYPE_CHOICES.unknown

    class Meta:
        model = Dish

    description = fuzzy.FuzzyText(length=150)
    price = fuzzy.FuzzyDecimal(1.5, 150)
    prep_time = timezone.timedelta(minutes=randint(15, 120))