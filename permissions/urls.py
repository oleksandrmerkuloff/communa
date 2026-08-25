from rest_framework import routers

from .views import PermissionsListView


router = routers.SimpleRouter()
router.register("", PermissionsListView.as_view(), basename="permission")

urlpatterns = router.urls
