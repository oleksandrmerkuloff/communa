import re

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_admin",
            "registered_at",
        )


class UserWriterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
        "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(**validated_data, password=password)

    def validate_email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.fullmatch(pattern, value):
            return value
        return serializers.ValidationError("Wrong email address.")

    def validate_phone_number(self, value):
        pattern = r"^(?:\+38)?(?:\(0\d{2}\)|0\d{2})\d{7}$"

        if re.fullmatch(pattern, value):
            return value

        return serializers.ValidationError("Wrong phone number.")

class UpdateUserSerializer(serializers.ModelSerializer):
    # add later validate email and phone_number
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name"
        )

    def validate_phone_number(self, value):
        pattern = r"^(?:\+38)?(?:\(0\d{2}\)|0\d{2})\d{7}$"

        if re.fullmatch(pattern, value):
            return value

        raise serializers.ValidationError("Wrong phone number.")


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user
