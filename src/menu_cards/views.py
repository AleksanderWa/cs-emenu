from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from menu_cards.models import Dish, MenuCard
from menu_cards.serializer import DishSerializer, MenuCardSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permissions_classes = [permissions.AllowAny]

    filterset_fields = ['id', 'name']
    ordering_fields = ('id', 'price', 'food_type')

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering')
        queryset = super().get_queryset()
        if ordering in self.ordering_fields:
            queryset = self.queryset.order_by(ordering)
        return queryset


class MenuCardViewSet(viewsets.ModelViewSet):
    queryset = MenuCard.objects.all().prefetch_related('dishes')
    serializer_class = MenuCardSerializer
    permissions_classes = [permissions.AllowAny]

    ordering_fields = ['id', 'name', 'dishes_num']

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering')
        queryset = super().get_queryset()
        queryset = self._annotate_dishes_num(queryset)
        if ordering in self.ordering_fields:
            queryset = self.queryset.order_by(ordering)
        return queryset

    @staticmethod
    def _annotate_dishes_num(queryset):
        return queryset.annotate(dishes_num=Count('dishes'))
