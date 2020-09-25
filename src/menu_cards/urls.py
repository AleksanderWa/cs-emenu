from rest_framework import routers

router = routers.DefaultRouter()
# router.register('stats', ArticleViewSet, 'statistics')
# router.register('authors', AuthorViewSet, 'authors')

urlpatterns = router.urls
