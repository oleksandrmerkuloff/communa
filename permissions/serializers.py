from rest_framework import serializers

from .models import Permission


class PermissionReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("code",)
        read_only_fields = ["code"]
