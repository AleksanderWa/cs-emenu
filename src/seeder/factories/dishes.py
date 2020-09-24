from menu_cards.models import Dish
from factory import (
    django,
    fuzzy,
)


class DishFactory(django.DjangoModelFactory):
    class Meta:
        model = Dish

    name = fuzzy.FuzzyText(length=4, prefix="Dish: ")
