from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import ApartmentMembership, Apartment
from users.serializers import UserReaderSerializer
from organization.serializers import OrganizationReaderSerializer


class ApartmentReaderSerializer(ModelSerializer):
    organization = OrganizationReaderSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = "__all__"


class ApartmentWriterSerializer(ModelSerializer):
    class Meta:
        model = Apartment
        fields = (
            "number",
            "organization",
        )


class ApartmentMembershipReaderSerializer(ModelSerializer):
    member = UserReaderSerializer(read_only=True)
    apartment = ApartmentReaderSerializer(read_only=True)

    class Meta:
        model = ApartmentMembership
        fields = "__all__"


class ApartmentMembershipWriterSerializer(ModelSerializer):
    class Meta:
        model = ApartmentMembership
        fields = (
            "role",
            "apartment",
            "member",
        )

    def validate(self, attrs):
        apartment = attrs.get("apartment")
        role = attrs.get("role")

        if (
            apartment
            and role == ApartmentMembership.ApartmentMembershipRoleChoice.HEAD
            and ApartmentMembership.objects.filter(
                apartment=apartment,
                role=ApartmentMembership.ApartmentMembershipRoleChoice.HEAD,
            ).exclude(pk=self.instance.pk if self.instance else None).exists()
        ):
            raise serializers.ValidationError("This apartment already has a head.")
        return attrs
