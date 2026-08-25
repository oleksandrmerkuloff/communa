from rest_framework import routers

from .views import RoleViewSet


router = routers.SimpleRouter()
router.register("", RoleViewSet.as_view(), basename="role")

urlpatterns = router.urls
