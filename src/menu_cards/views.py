from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from menu_cards.models import Dish, MenuCard
from menu_cards.serializer import DishSerializer, MenuCardSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permissions_classes = [permissions.AllowAny]

    # def list(self, request, *args, **kwargs):
    #     authors = Dish.objects.all()
    #     serializer = DishSerializer(authors, many=True)
    #     return Response(serializer.data)

class MenuCardViewSet(viewsets.ModelViewSet):
    queryset = MenuCard.objects.all()
    serializer_class = MenuCardSerializer
    permissions_classes = [permissions.AllowAny]

