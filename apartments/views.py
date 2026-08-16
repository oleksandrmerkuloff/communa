from rest_framework.viewsets import ModelViewSet

from .models import ApartmentMembership, Apartment
from .serializers import (
    ApartmentReaderSerializer,
    ApartmentMembershipReaderSerializer,
    ApartmentWriterSerializer,
    ApartmentMembershipWriterSerializer,
)


class ApartmentViewSet(ModelViewSet):
    queryset = Apartment.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ApartmentReaderSerializer
        return ApartmentWriterSerializer


class ApartmentMembershipViewSet(ModelViewSet):
    queryset = ApartmentMembership

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ApartmentMembershipReaderSerializer
        return ApartmentMembershipWriterSerializer
