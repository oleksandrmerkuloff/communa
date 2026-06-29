from rest_framework import routers

from .views import TagViewSet, PostViewSet, NewsAttachmentViewSet


router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'attachments', NewsAttachmentViewSet)


urlpatterns = router.urls
