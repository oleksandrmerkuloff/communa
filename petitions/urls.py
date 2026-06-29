from rest_framework.routers import SimpleRouter

from .views import PetitionViewSet, VoteViewSet


router = SimpleRouter()
router.register("petitions", PetitionViewSet)
router.register("votes", VoteViewSet)

urlpatterns = router.urls
