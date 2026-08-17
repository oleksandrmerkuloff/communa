import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from organization.models import Organization
from core.mixins import TimestampMixin


User = get_user_model()


class Apartment(TimestampMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    number = models.PositiveIntegerField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="apartments"
    )

    def __str__(self) -> str:
        return (
            f"Organization: {self.organization.name}. Apartment number: {self.number}."
        )

    class Meta:
        verbose_name = "Apartment"
        verbose_name_plural = "Apartments"
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["number", "organization"],
                name="unique_number_apartment",
            )
        ]


#! Add validation for head role. 1 ap == one head
class ApartmentMembership(TimestampMixin):
    class ResidentRoleChoice(models.TextChoices):
        HEAD = "H", _("Head")
        RESIDENT = "R", _("Resident")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role = models.CharField(
        max_length=1,
        choices=ResidentRoleChoice.choices,
        default=ResidentRoleChoice.RESIDENT,
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="residents"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="residents")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} from apartment number {self.apartment.number}."

    class Meta:
        verbose_name = "Apartment Resident"
        verbose_name_plural = "Apartment Residents"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "apartment"],
                name="unique_apartment_resident",
            )
        ]
