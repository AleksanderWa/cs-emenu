from rest_framework import serializers

from menu_cards.models import Dish, MenuCard
from utils import DynamicFieldsModelSerializer


class MenuCardSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MenuCard
        fields = ['id', 'name', 'description']


class DishSerializer(DynamicFieldsModelSerializer):
    menu_card = MenuCardSerializer(fields={'name'})
    class Meta:
        model = Dish
        fields = [
            'id',
            'name',
            'description',
            'price',
            'prep_time',
            'food_type',
            'menu_card',
        ]


