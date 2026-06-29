from rest_framework.routers import SimpleRouter

from .views import MembershipViewSet


router = SimpleRouter()
router.register(r"members", MembershipViewSet)

urlpatterns = router.urls
