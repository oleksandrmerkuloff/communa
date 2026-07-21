from rest_framework.viewsets import ModelViewSet

from .models import Organization
from .serializers import OrganizationWriterSerializer, OrganizationReaderSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()

    def get_queryset(self):
        return (
            Organization.objects
            .filter(memberships__member=self.request.user)
            .distinct()
        )
        

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrganizationReaderSerializer
        return OrganizationWriterSerializer
