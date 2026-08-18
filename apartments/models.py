import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Q

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


class ApartmentMembership(TimestampMixin):
    class ApartmentMembershipRoleChoice(models.TextChoices):
        HEAD = "H", _("Head")
        RESIDENT = "R", _("Resident")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role = models.CharField(
        max_length=1,
        choices=ApartmentMembershipRoleChoice.choices,
        default=ApartmentMembershipRoleChoice.RESIDENT,
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="memberships"
    )
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apartment_memberships")

    def __str__(self) -> str:
        return f"{self.member.first_name} {self.member.last_name} from apartment number {self.apartment.number}."

    class Meta:
        verbose_name = "Apartment Membership"
        verbose_name_plural = "Apartment Memberships"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "apartment"],
                name="unique_apartment_resident",
            ),
            models.UniqueConstraint(
                fields=["apartment"],
                condition=Q(role=ResidentRoleChoice.HEAD),
                name="unique_apartment_head",
            ),
        ]
