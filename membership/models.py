import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from organization.models import Organization


User = get_user_model()


class Membership(models.Model):
    class MemberRole(models.TextChoices):
        RESIDENT = "R", _("Resident")
        SECRETARY = "S", _("Secretary")
        ACCOUNTANT = "A", _("Accountant")
        VICE_HEAD = "V", _("Vice Head")
        HEAD = "H", _("Head")
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role = models.CharField(max_length=1, choices=MemberRole, default=MemberRole.RESIDENT)
    apartment_number = models.PositiveSmallIntegerField()
    can_vote = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name="memberships", on_delete=models.CASCADE)

    def __str__(self):
        full_name = self.member.get_full_name()
        return f"{full_name} ({self.organization.name})"

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ["organization", "role", "-registered_at"]
        constraints = [
        models.UniqueConstraint(
            fields=["member", "organization"],
            name="unique_member_organization",
        )
    ]
