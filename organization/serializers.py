from rest_framework import serializers

from .models import Organization


class OrganizationReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ["id"]


class OrganizationWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "country", "city", "street_address", "post_index", "description"]