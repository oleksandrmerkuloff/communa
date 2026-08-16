from rest_framework.routers import SimpleRouter

from .views import ApartmentViewSet, ApartmentMembershipViewSet


router = SimpleRouter()
router.register("", ApartmentViewSet, basename="apartment")
router.register(
    r"memberships", ApartmentMembershipViewSet, basename="apartment-membership"
)

urlpatterns = router.urls
