from rest_framework import serializers

from .models import User


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id"
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "registered_at",
        )


class UserWriterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        )
        extra_kwargs = {
        "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        return User.objects.create_user(validated_data, password=password)
