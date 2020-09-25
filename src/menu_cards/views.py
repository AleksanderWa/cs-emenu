from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from menu_cards.models import Dish
from menu_cards.serializer import DishSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def list(self, request, *args, **kwargs):
        authors = Dish.objects.all()
        #serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)