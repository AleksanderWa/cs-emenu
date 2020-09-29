from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import (
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

from menu_cards.models import Dish, MenuCard
from utils import DynamicFieldsModelSerializer


class DishSerializer(DynamicFieldsModelSerializer):

    menu_card_id = PrimaryKeyRelatedField(
        queryset=MenuCard.objects.all(), required=False
    )
    menu_card = SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'

    @staticmethod
    def get_menu_card(obj):
        if obj.menu_card:
            return obj.menu_card.name


class MenuCardSerializer(DynamicFieldsModelSerializer):
    dishes = DishSerializer(many=True)
    dishes_num = ReadOnlyField()

    class Meta:
        model = MenuCard
        fields = [
            'id',
            'name',
            'description',
            'dishes',
            'dishes_num',
            'created',
            'modified',
        ]

    def validate_dishes(self, data):
        self._validate_dish_names_and_type(data)
        return data

    @staticmethod
    def _validate_dish_names_and_type(data):
        name_food_dish = [
            (dish.get('name'), dish.get('food_type')) for dish in data
        ]
        if len(name_food_dish) != len(set(name_food_dish)):
            raise ValidationError('List contains duplicated dish names')

    def create(self, validated_data):
        dishes = validated_data.pop('dishes')
        menu_card = super().create(validated_data)
        for dish in dishes:
            Dish.objects.create(menu_card=menu_card, **dish)
        return menu_card
