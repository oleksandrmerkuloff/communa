from rest_framework import routers

from .views import TagViewSet, PostViewSet, NewsAttachmentViewSet


router = routers.SimpleRouter()
router.register(r'', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'attachments', NewsAttachmentViewSet, basename='attachment')


urlpatterns = router.urls
