from rest_framework.viewsets import ModelViewSet

from .models import Membership
from .serializers import MembershipReaderSerializer, MembershipWriterSerializer
from .permissions import CanCreateMembership, CanViewMembership, CanEditMembership, CanDeleteMembership


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [CanViewMembership]
        elif self.action == "create":
            self.permission_classes = [CanCreateMembership]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditMembership]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteMembership]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return (
            Membership.objects
            .filter(member=self.request.user)
            .select_related("member", "organization")
        )
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return MembershipReaderSerializer
        return MembershipWriterSerializer
