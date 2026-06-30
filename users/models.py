from django.contrib.auth.models import AbstractUser
from django.db import models


# Add custom validation for user phone

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    phone_number = models.CharField(
        max_length=25,
        unique=True,
        blank=True,
        null=True,
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = None

    def __str__(self):
        return self.email
