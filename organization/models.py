import uuid

from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=75)
    country = models.CharField(max_length=75, default="Ukraine")
    city = models.CharField(max_length=75)
    street_address = models.CharField(max_length=150)
    post_index = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def address(self):
        return f"{self.street_address}\n{self.city}\n{self.country}\n{self.post_index}"

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["-created_at"]
