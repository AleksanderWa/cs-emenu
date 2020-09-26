from rest_framework.fields import ReadOnlyField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from menu_cards.models import Dish, MenuCard
from utils import DynamicFieldsModelSerializer


class DishSerializer(DynamicFieldsModelSerializer):

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
        fields = ['id', 'name', 'description', 'dishes', 'dishes_num']

    def create(self, validated_data):
        dishes = validated_data.pop('dishes')
        menu_card = MenuCard.objects.create(**validated_data)
        for dish in dishes:
            Dish.objects.create(menu_card=menu_card, **dish)
        return menu_card
