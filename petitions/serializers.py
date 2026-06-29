from rest_framework.serializers import ModelSerializer

from .models import Petition, PetitionVote
from organization.serializers import OrganizationReaderSerializer
from users.serializers import UserReaderSerializer


class VoteSerializer(ModelSerializer):
    class Meta:
        model = PetitionVote
        fields = "__all__"
        read_only_fields = ["id"]


class PetitionWriterSerializer(ModelSerializer):
    class Meta:
        model = Petition
        fields = ("topic", "content", "status", "author", "organization")


class PetitionReaderSerializer(ModelSerializer):
    author = UserReaderSerializer(read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    class Meta:
        model = Petition
        fields = "__all__"
