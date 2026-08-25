import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.mixins import TimestampMixin
from organization.models import Organization
from roles.models import Role
from apartments.models import Apartment


User = get_user_model()


class Membership(TimestampMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="memberhips")
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT, related_name="memberships")
    member = models.ForeignKey(
        User, related_name="memberships", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization, related_name="memberships", on_delete=models.CASCADE
    )

    def __str__(self):
        full_name = self.member.get_email_field_name()
        return f"{full_name} ({self.organization.name})"

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ["organization", "role", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "organization"],
                name="unique_member_organization",
            )
        ]
