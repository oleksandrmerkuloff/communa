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
    user = UserReaderSerializer(read_only=True)
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
            "user",
        )
