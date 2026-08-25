from rest_framework.viewsets import ModelViewSet

from .models import Role
from .serializers import RoleReaderSerializer, RoleWriterSerializer


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()

    def get_permissions(self):
        return super().get_permissions()

    def get_queryset(self):
        return (
            Role.objects.filter(organization__memberships__member=self.request.user)
            .select_related("organization")
            .prefetch_related("permissions")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RoleReaderSerializer
        return RoleWriterSerializer
