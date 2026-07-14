from rest_framework.routers import SimpleRouter

from .views import MembershipViewSet


router = SimpleRouter()
router.register(r"", MembershipViewSet, basename="organization")

urlpatterns = router.urls
