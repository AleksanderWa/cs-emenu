from menu_cards.models import MenuCard
from factory import (
    django,
    fuzzy,
    Sequence,
)


class MenuCardsFactory(django.DjangoModelFactory):
    class Meta:
        model = MenuCard

    name = Sequence(lambda n: f"Menu card : {n}")
    description = fuzzy.FuzzyText(length=150)
