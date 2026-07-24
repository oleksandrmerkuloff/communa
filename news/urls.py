from rest_framework import routers

from .views import TagViewSet, PostViewSet


router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')


urlpatterns = router.urls
