from rest_framework.viewsets import ModelViewSet

from .models import Membership
from .serializers import MembershipReaderSerializer, MembershipWriterSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()

    def get_queryset(self):
        return (
            Membership.objects
            .select_related("member", "organization")
        )
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return MembershipReaderSerializer
        return MembershipWriterSerializer
