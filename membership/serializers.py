from rest_framework.serializers import ModelSerializer

from .models import Membership


class MembershipReaderSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class MembershipWriterSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ["role", "apartment_number", "can_vote", "member", "organization"]
