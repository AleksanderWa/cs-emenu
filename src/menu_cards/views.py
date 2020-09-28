from django.db.models import Count
from rest_framework import viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)
from rest_framework.permissions import IsAuthenticated

from menu_cards.models import Dish, MenuCard
from menu_cards.serializer import DishSerializer, MenuCardSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    filterset_fields = ['id', 'name', 'created', 'modified']
    ordering_fields = ['id', 'name', 'dishes_num']

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering')
        queryset = self._annotate_dishes_num(self.queryset)
        if ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        return queryset

    @staticmethod
    def _annotate_dishes_num(queryset):
        return queryset.annotate(dishes_num=Count('dishes'))

    #
    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.queryset.get(pk=kwargs.get('pk'))
    #     serializer = self.serializer_class(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(f"PARTIAL UPDATE!")
    #     return Response(serializer.data)
