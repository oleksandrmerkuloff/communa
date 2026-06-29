import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Petition(models.Model):
    class PetitionStatus(models.TextChoices):
        DELIVERED = "D", _("Delivered")
        CONSIDERATION = "C", _("Consideration")
        ACCEPTED = "A", _("Accepted")
        REJECTED = "R", _("Rejected")

    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    topic = models.CharField(max_length=50)
    content = models.TextField()
    status = models.CharField(choices=PetitionStatus, max_length=1, default=PetitionStatus.DELIVERED)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="petitions")
    organization = models.ForeignKey("Organization", related_name="petitions", on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ["-created_at",]
        verbose_name = "Petition"
        verbose_name_plural = "Petitions"
