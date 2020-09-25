from rest_framework import serializers

from menu_cards.models import Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'prep_time', 'food_type']