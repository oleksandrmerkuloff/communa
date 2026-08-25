from rest_framework.serializers import ModelSerializer

from .models import Membership
from users.serializers import UserReaderSerializer
from organization.serializers import OrganizationReaderSerializer
from apartments.serializers import ApartmentReaderSerializer


class MembershipReaderSerializer(ModelSerializer):
    member = UserReaderSerializer(read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    apartment = ApartmentReaderSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = "__all__"


class MembershipWriterSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ["role", "apartment", "member", "organization"]
