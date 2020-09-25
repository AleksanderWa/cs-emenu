from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from menu_cards.views import DishViewSet

router = routers.DefaultRouter()
router.register('dishes', DishViewSet, basename='dishes')

urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1'))
]
