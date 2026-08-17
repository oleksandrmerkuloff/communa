import re

from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


def validate_phone_number(value):
    pattern = r"^(?:\+38)?(?:\(0\d{2}\)|0\d{2})\d{7}$"
    if re.fullmatch(pattern, value):
        return value
    raise serializers.ValidationError("Wrong phone number.")


def validate_email(value):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(pattern, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    raise serializers.ValidationError("Wrong email address.")
