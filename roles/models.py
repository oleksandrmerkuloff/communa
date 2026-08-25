import uuid

from django.db import models

from core.mixins import TimestampMixin
from organization.models import Organization
from permissions.models import Permission


class Role(TimestampMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    is_system = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, related_name="roles")

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("name", "organization",),
                name="unique_role_per_organization"
            ),
        ]
