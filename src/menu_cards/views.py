from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from menu_cards.models import Dish, MenuCard
from menu_cards.serializer import (DishPhotoSerializer, DishSerializer,
                                   MenuCardSerializer)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ["id", "name"]
    ordering_fields = ("id", "price", "food_type")

    def get_queryset(self):
        ordering = self.request.query_params.get("ordering")
        queryset = super().get_queryset()
        if ordering in self.ordering_fields:
            queryset = self.queryset.order_by(ordering)
        return queryset

    @action(
        methods=["post"],
        detail=True,
        url_path="photo",
        url_name="photo",
        parser_classes=[MultiPartParser],
        serializer_class=DishPhotoSerializer,
    )
    def add_photo(self, request, pk):
        obj = get_object_or_404(Dish, id=pk)
        data = request.data
        data["dish"] = obj.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class MenuCardViewSet(viewsets.ModelViewSet):
    queryset = MenuCard.objects.all().prefetch_related("dishes")
    serializer_class = MenuCardSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ["id", "name", "created", "modified"]
    ordering_fields = ["id", "name", "dishes_num"]

    def get_queryset(self):
        ordering = self.request.query_params.get("ordering")
        queryset = self._annotate_dishes_num(self.queryset)
        if ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        return queryset

    @staticmethod
    def _annotate_dishes_num(queryset):
        return queryset.annotate(dishes_num=Count("dishes"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.copy())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
