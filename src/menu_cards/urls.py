from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from menu_cards.views import DishViewSet, MenuCardViewSet

router = routers.DefaultRouter()
router.register('dishes', DishViewSet, basename='dishes')
router.register('menu', MenuCardViewSet, basename='menus')

urlpatterns = [
    url(r'^', include(router.urls)),
]
