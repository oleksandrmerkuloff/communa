from rest_framework import serializers

from .models import User


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "groups",
            "user_permissions",
        )


class UserWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )


class SelfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
