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
from roles.models import Role


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

    def perform_create(self, serializer):
        with transaction.atomic():
            organization = serializer.save()

            head_role = Role.objects.filter(
                organization=organization, 
                name="Голова ОСББ"
            ).first()

            if not head_role:
                head_role = Role.objects.create(
                    organization=organization,
                    name="Голова ОСББ",
                    is_system=True
                )

            Membership.objects.create(
                member=self.request.user,
                organization=organization,
                role=head_role,
            )
