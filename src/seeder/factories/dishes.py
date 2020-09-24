import factory
from random import randint

from django.utils import timezone

from menu_cards.models import Dish, FOOD_TYPE_CHOICES
from factory import (
    django,
    fuzzy,
    Sequence,
)

FOOD_TYPE_IDS = [x[0] for x in FOOD_TYPE_CHOICES]


class DishFactory(django.DjangoModelFactory):
    class Meta:
        model = Dish

    name = factory.Faker('sentence', nb_words=4)#Sequence(lambda n: f"Dish_{n}")
    description = fuzzy.FuzzyText(length=150)
    price = fuzzy.FuzzyDecimal(1.5, 150)
    prep_time = timezone.timedelta(minutes=randint(15, 120))
    food_type = fuzzy.FuzzyChoice(FOOD_TYPE_IDS)
