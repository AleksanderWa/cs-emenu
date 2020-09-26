from rest_framework import viewsets, permissions

from menu_cards.models import Dish, MenuCard
from menu_cards.serializer import DishSerializer, MenuCardSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permissions_classes = [permissions.AllowAny]

    filter_fields = [
        'id',
        'name',
        'description',
        'price',
        'prep_time',
        'menu_card',
        'food_type',
    ]
    # def list(self, request, *args, **kwargs):
    #     authors = Dish.objects.all()
    #     serializer = DishSerializer(authors, many=True)
    #     return Response(serializer.data)


class MenuCardViewSet(viewsets.ModelViewSet):
    queryset = MenuCard.objects.all().prefetch_related('dishes')
    serializer_class = MenuCardSerializer
    permissions_classes = [permissions.AllowAny]
