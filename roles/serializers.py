from django.db import transaction
from rest_framework import serializers

from .models import Role
from organization.serializers import OrganizationReaderSerializer
from permissions.serializers import PermissionReaderSerializer


class RoleReaderSerializer(serializers.ModelSerializer):
    organization = OrganizationReaderSerializer(read_only=True)
    permissions = PermissionReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class RoleWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "organization", "permissions",)

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])

        with transaction.atomic():
            role = Role.objects.create(**validated_data)
            role.permissions.set(permissions)
        return role

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions", [])

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if permissions:
                instance.permissions.set(permissions)

        return instance
