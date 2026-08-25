from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Organization
from .serializers import OrganizationWriterSerializer, OrganizationReaderSerializer
from .permissions import (
    CanCreateOrganization,
    CanEditOrganization,
    CanDeleteOrganization,
)
from membership.models import Membership


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [CanCreateOrganization]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditOrganization]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteOrganization]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__member=self.request.user
        ).distinct()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrganizationReaderSerializer
        return OrganizationWriterSerializer

    # Here I need change head assign logic
    def perform_create(self, serializer):
        apartment_number = self.request.data.get("apartment_number")

        with transaction.atomic():
            organization = serializer.save()

            Membership.objects.create(
                member=self.request.user,
                organization=organization,
                apartment_number=apartment_number,
                role=Membership.MemberRole.HEAD,
            )
