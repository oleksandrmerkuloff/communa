from rest_framework import serializers

from .models import User


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
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
    
    def create(self, validated_data):
        password = validated_data.pop("password", None)

        return User.objects.create(validated_data, password)


class SelfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
