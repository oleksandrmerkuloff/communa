from rest_framework import serializers

from .models import Permission


class PermissionReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["code", "name"]
