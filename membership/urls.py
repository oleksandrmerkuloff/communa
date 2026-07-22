from rest_framework.routers import SimpleRouter

from .views import MembershipViewSet


router = SimpleRouter()
router.register(r"", MembershipViewSet, basename="membership")

urlpatterns = router.urls
